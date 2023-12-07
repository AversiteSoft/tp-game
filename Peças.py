""" Importa a biblioteca pygame. """
import pygame

"""Classe que representa uma peça do jogo de xadrez."""
class Piece:
    

    """
        Construtor da classe Piece.
        Args:
            pos (tuple): Posição da peça no tabuleiro (x, y).
            color (str): Cor da peça ('branca' ou 'preta').
            board (Board): Tabuleiro em que a peça está localizada.
    """
    def __init__(self, pos, color, board):
        
        self.pos = pos  # Posição da peça no tabuleiro
        self.x = pos[0]  # Coordenada x da posição
        self.y = pos[1]  # Coordenada y da posição
        self.color = color  # Cor da peça
        self.has_moved = False  # Flag indicando se a peça já se moveu

    def move(self, board, square, force=False):
        """
        Move a peça para a posição especificada pelo tabuleiro.

        Args:
            board (Board): Tabuleiro em que a peça está localizada.
            square (Square): Quadrado para onde a peça será movida.
            force (bool, opcional): Força a movimentação, ignorando regras de movimento.

        Returns:
            bool: True se a movimentação foi bem-sucedida, False caso contrário.
        """
        for i in board.squares:
            i.highlight = False  # Desativa o efeito de destaque em todas as casas

        if square in self.get_valid_moves(board) or force:
            # Movimentação permitida

            prev_square = board.get_square_from_pos(self.pos)  # Obtenção da casa anterior
            self.pos, self.x, self.y = square.pos, square.x, square.y  # Atualização da posição da peça

            # Atualização do tabuleiro e da peça selecionada
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True

            # Promoção de peão (se aplicável)
            if self.notation == ' ':  # Se a peça for um peão
                if self.y == 0 or self.y == 7:  # Se o peão alcançou a borda do tabuleiro
                    # from data.classes.pieces.Queen import Queen  # Importação da classe rainha
                    square.occupying_piece = Queen(  # Criação de uma nova rainha
                        (self.x, self.y),  # Posição da rainha
                        self.color,  # Cor da rainha
                        board  # Tabuleiro
                    )  # Atribuição da rainha à casa

            # Rocha (se aplicável)
            if self.notation == 'K':
                if prev_square.x - self.x == 2:  # Movimento do rei para a direita
                    rook = board.get_piece_from_pos((0, self.y))  # Obter a torre
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)  # Movimentá-la dois casas à direita
                elif prev_square.x - self.x == -2:  # Movimento do rei para a esquerda
                    rook = board.get_piece_from_pos((7, self.y))  # Obter a torre
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)  # Movimentá-la dois casas à esquerda

            return True  # Movimentação bem-sucedida
        else:
            # Movimentação inválida
            board.selected_piece = None
            return False

    # Métodos de geração de movimentos possíveis e válidos

    def get_moves(self, board):
        """
        Obtém a lista de movimentos possíveis para a peça.

        Args:
            board (Board): Tabuleiro em que a peça está localizada.

        Returns:
            list(Square): Lista de quadrados possíveis para a peça se mover.
        """
        output = []
        for direction in self.get_possible_moves(board):
             for square in direction:  # Itera pelas casas na direção especificada
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:  # Verifica se a casa está ocupada por uma peça aliada
                        break  # Interrompe o laço caso encontre peça aliada
                    else:  # Caso a casa esteja ocupada por uma peça inimiga
                        output.append(square)  # Adiciona a casa à lista de movimentos possíveis
                        break  # Interrompe o laço caso encontre a primeira casa válida
                else:  # Caso a casa esteja vazia
                    output.append(square)  # Adiciona a casa à lista de movimentos possíveis

        return output  # Retorna a lista de movimentos possíveis

    def get_valid_moves(self, board):
        """
        Obtém a lista de movimentos válidos para a peça, considerando a regra de não colocar o rei em cheque.

        Args:
            board (Board): Tabuleiro em que a peça está localizada.

        Returns:
            list(Square): Lista de quadrados possíveis para a peça se mover, respeitando a regra de não enchercar o rei.
        """
        output = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)

        return output  # Retorna a lista de movimentos válidos

    def attacking_squares(self, board):
        """
        Obtém a lista de quadrados que a peça pode atacar (abarcar).

        Args:
            board (Board): Tabuleiro em que a peça está localizada.

        Returns:
            list(Square): Lista de quadrados que a peça pode atacar.
        """
        return self.get_moves(board)  # True para todas as peças exceto peão
