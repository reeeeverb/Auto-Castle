import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.lang.builder import Builder
#from watchpoints import watch


class ChessGame(Widget):
    s_width = NumericProperty(Window.width)
    s_height = NumericProperty(Window.height)
    pass


class Chessboard(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.down_square = (0,0)
        self.up_square = (0,0)
        self.names, self.color, self.piece = ["EMPTY"]*64, ["EMPTY"]*64, ["EMPTY"]*64
        p_size = ObjectProperty(0)
        x = ObjectProperty()
        y = ObjectProperty()
        self.marker_present = False
        self.widget_list = []
        self.current_move = "WHITE"
        self.first = True
        self.white_capture = []
        self.black_capture = []
        self.move = 0
        self.forward = "WHITE"

    def on_touch_down(self, touch):
        if self.first:
            self.first = False
            self.reset_board()
        self.parent.w_king1.inCheck()
        self.parent.b_king1.inCheck()
        if self.collide_point(*touch.pos):
            xpos = touch.pos[0]-self.pos[0]
            ypos = touch.pos[1]-self.pos[1]
            self.down_square = self.square_pos(xpos,ypos)
            if self.down_square != self.up_square:
                self.clear_markers()
            ## Testing

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            xpos = touch.pos[0]-self.pos[0]
            ypos = touch.pos[1]-self.pos[1]
            self.up_square = self.square_pos(xpos,ypos)
            if self.up_square == self.down_square and self.piece[self.up_square[2] != "EMPTY"]:
                self.generate_moves(self.down_square,True)
            else:
                self.clear_markers()
                if self.legal_move(self.down_square, self.up_square):
                    current_piece = (self.names[self.down_square[2]])
                    current_piece.set(self.up_square[0],self.up_square[1])
                    self.current_move_swap()

    def clear_markers(self):
        if self.marker_present:
            #self.remove_widget(self.new_red)
            #self.remove_widget(self.new_red)
            for widget in self.widget_list:
                self.remove_widget(widget)
            self.widget_list = []
            self.marker_present=False

    def generate_moves(self,square,show_moves=False):
        forward = self.forward
        piece = self.piece[square[2]]
        color = self.color[square[2]]
        out = []
        ## TO DO: Implement en passant and promotion
        if piece == "PAWN":
            if color == forward:
                if self.piece[square[2]+8] == "EMPTY":
                    if show_moves == True:
                        self.show_moves(square[0]+1,square[1])
                    else:
                        out.append(square[2]+8)
                    if square[0] < 6 and self.piece[square[2]+16] == "EMPTY" and square[0] == 1:
                        if show_moves == True:
                            self.show_moves(square[0]+2,square[1])
                        else:
                            out.append(square[2]+16)
                if square[1] != 0 and self.piece[square[2]+7] != "EMPTY" and color != self.color[square[2]+7]:
                    if show_moves == True:
                        self.show_moves(square[0]+1,square[1]-1)
                    else:
                        out.append(square[2]+7)
                if square[1] != 7 and self.piece[square[2]+9] != "EMPTY" and color != self.color[square[2]+9]:
                    if show_moves == True:
                        self.show_moves(square[0]+1,square[1]+1)
                    else:
                        out.append(square[2]+9)
                if square[1] != 7 and self.piece[square[2]-1] == "PAWN" and self.names[square[2]-1].en_passantable_move == self.move and color != self.color[square[2]-1]:
                    if show_moves == True:
                        self.show_moves(square[0]+1,square[1]-1)
                    else:
                        out.append(square[2]+7)
                if square[1] != 7 and self.piece[square[2]+1] == "PAWN" and self.names[square[2]+1].en_passantable_move == self.move and color != self.color[square[2]+1]:
                    if show_moves == True:
                        self.show_moves(square[0]+1,square[1]+1)
                    else:
                        out.append(square[2]+9)
            else:
                if self.piece[square[2]-8] == "EMPTY":
                    if show_moves == True:
                        self.show_moves(square[0]-1,square[1])
                    else:
                        out.append(square[2]-8)
                    if square[0] > 1 and self.piece[square[2]-16] == "EMPTY" and square[0] == 6:
                        if show_moves == True:
                            self.show_moves(square[0]-2,square[1])
                        else:
                            out.append(square[2]-16)
                if square[1] != 7 and self.piece[square[2]-7] != "EMPTY" and color != self.color[square[2]-7]:
                    if show_moves == True:
                        self.show_moves(square[0]-1,square[1]+1)
                    else:
                        out.append(square[2]-7)
                if square[1] != 0 and self.piece[square[2]-9] != "EMPTY" and color != self.color[square[2]-9]:
                    if show_moves == True:
                        self.show_moves(square[0]-1,square[1]-1)
                    else:
                        out.append(square[2]-9)
                if square[1] != 7 and self.piece[square[2]-1] == "PAWN" and self.names[square[2]-1].en_passantable_move == self.move and color != self.color[square[2]-1]:
                    if show_moves == True:
                        self.show_moves(square[0]-1,square[1]-1)
                    else:
                        out.append(square[2]-9)
                if square[1] != 7 and self.piece[square[2]+1] == "PAWN" and self.names[square[2]+1].en_passantable_move == self.move and color != self.color[square[2]+1]:
                    if show_moves == True:
                        self.show_moves(square[0]-1,square[1]+1)
                    else:
                        out.append(square[2]-7)
        elif piece == "KNIGHT":
            if square[1] > 0 and square[0] < 6 and self.color[square[2]+15] != color:
                if show_moves == True:
                    self.show_moves(square[0]+2,square[1]-1)
                else:
                    out.append(square[2]+15)
            if square[1] < 7 and square[0] < 6 and self.color[square[2]+17] != color:
                if show_moves == True:
                    self.show_moves(square[0]+2,square[1]+1)
                else:
                    out.append(square[2]+17)
            if square[1] > 1 and square[0] < 7 and self.color[square[2]+6] != color:
                if show_moves == True:
                    self.show_moves(square[0]+1,square[1]-2)
                else:
                    out.append(square[2]+6)
            if square[1] < 6 and square[0] < 7 and self.color[square[2]+10] != color:
                if show_moves == True:
                    self.show_moves(square[0]+1,square[1]+2)
                else:
                    out.append(square[2]+10)
            if square[1] > 0 and square[0] > 1 and self.color[square[2]-17] != color:
                if show_moves == True:
                    self.show_moves(square[0]-2,square[1]-1)
                else:
                    out.append(square[2]-17)
            if square[1] < 7 and square[0] > 1 and self.color[square[2]-15] != color:
                if show_moves == True:
                    self.show_moves(square[0]-2,square[1]+1)
                else:
                    out.append(square[2]-15)
            if square[1] > 1 and square[0] > 0 and self.color[square[2]-10] != color:
                if show_moves == True:
                    self.show_moves(square[0]-1,square[1]-2)
                else:
                    out.append(square[2]-10)
            if square[1] < 6 and square[0] > 0 and self.color[square[2]-6] != color:
                if show_moves == True:
                    self.show_moves(square[0]-1,square[1]+2)
                else:
                    out.append(square[2]-6)
        if piece == "BISHOP" or piece == "QUEEN":
            t_square1 = square[1]-1
            t_square0 = square[0]-1
            t_tracker = square[2]-9
            dont_stop = True
            while t_square1 >= 0 and t_square0 >= 0 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 -= 1
                t_square0 -= 1
                t_tracker -= 9
            t_square1 = square[1]+1
            t_square0 = square[0]+1
            t_tracker = square[2]+9
            dont_stop = True
            while t_square1 <= 7 and t_square0 <= 7 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 += 1
                t_square0 += 1
                t_tracker += 9
            t_square1 = square[1]-1
            t_square0 = square[0]+1
            t_tracker = square[2]+7
            dont_stop = True
            while t_square1 >= 0 and t_square0 <= 7 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 -= 1
                t_square0 += 1
                t_tracker += 7
            t_square1 = square[1]+1
            t_square0 = square[0]-1
            t_tracker = square[2]-7
            dont_stop = True
            while t_square1 <= 7 and t_square0 >= 0 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 += 1
                t_square0 -= 1
                t_tracker -= 7
        if piece == "ROOK" or piece == "QUEEN":
            t_square1 = square[1]-1
            t_square0 = square[0]
            t_tracker = square[2]-1
            dont_stop = True
            while t_square1 >= 0 and t_square0 >= 0 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 -= 1
                t_tracker -= 1
            t_square1 = square[1]+1
            t_square0 = square[0]
            t_tracker = square[2]+1
            dont_stop = True
            while t_square1 <= 7 and t_square0 <= 7 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square1 += 1
                t_tracker += 1
            t_square1 = square[1]
            t_square0 = square[0]-1
            t_tracker = square[2]-8
            dont_stop = True
            while t_square1 >= 0 and t_square0 >= 0 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square0 -= 1
                t_tracker -= 8
            t_square1 = square[1]
            t_square0 = square[0]+1
            t_tracker = square[2]+8
            dont_stop = True
            while t_square1 <= 7 and t_square0 <= 7 and dont_stop:
                if self.color[t_tracker] == color:
                    break
                elif self.color[t_tracker] != color and self.color[t_tracker] != "EMPTY":
                    dont_stop = False
                if show_moves == True:
                    self.show_moves(t_square0,t_square1)
                else:
                    out.append(t_tracker)
                t_square0 += 1
                t_tracker += 8
        if piece == "KING":
            # Check for castling
            if self.names[square[2]].castleable:
                if self.piece[square[2]-4] == "ROOK" and self.names[square[2]-4].castleable:
                    if self.piece[square[2]-3] == "EMPTY" and self.piece[square[2]-2] == "EMPTY" and self.piece[square[2]-1] == "EMPTY":
                        if show_moves:
                            self.show_moves(square[0],square[1]-2)
                        else:
                            out.append(square[2]-2)
                if self.piece[square[2]+3] == "ROOK" and self.names[square[2]+3].castleable:
                    if self.piece[square[2]+2] == "EMPTY" and self.piece[square[2]+1] == "EMPTY":
                        if show_moves:
                            self.show_moves(square[0],square[1]+2)
                        else:
                            out.append(square[2]+2)

            if square[1] < 7 and self.color[square[2]+1] != color:
                if show_moves:
                    self.show_moves(square[0],square[1]+1)
                else:
                    out.append(square[2]+1)
            if square[1] > 0 and self.color[square[2]-1] != color:
                if show_moves:
                    self.show_moves(square[0],square[1]-1)
                else:
                    out.append(square[2]-1)
            if square[0] < 7 and square[1] > 0 and self.color[square[2]+7] != color:
                if show_moves:
                    self.show_moves(square[0]+1,square[1]-1)
                else:
                    out.append(square[2]+7)
            if square[0] < 7 and self.color[square[2]+8] != color:
                if show_moves:
                    self.show_moves(square[0]+1,square[1])
                else:
                    out.append(square[2]+8)
            if square[0] < 7 and square[1] < 7 and self.color[square[2]+9] != color:
                if show_moves:
                    self.show_moves(square[0]+1,square[1]+1)
                else:
                    out.append(square[2]+9)
            if square[0] > 0 and square[1] < 7 and self.color[square[2]-7] != color:
                if show_moves:
                    self.show_moves(square[0]-1,square[1]+1)
                else:
                    out.append(square[2]-7)
            if square[0] > 0 and self.color[square[2]-8] != color:
                if show_moves:
                    self.show_moves(square[0]-1,square[1])
                else:
                    out.append(square[2]-8)
            if square[0] > 0 and square[1] > 0 and self.color[square[2]-9] != color:
                if show_moves:
                    self.show_moves(square[0]-1,square[1]-1)
                else:
                    out.append(square[2]-9)

        return out;

    def show_moves(self, row, column):
        #row = 1
        #column = 6
        self.new_red = Image(source='chess-pieces/red-circle.png',pos=(self.x+self.p_size*column,self.y+self.p_size*row),size=(self.p_size,self.p_size))
        self.add_widget(self.new_red)
        self.widget_list.append(self.new_red)
        self.marker_present=True

    def reset_board(self):
        self.current_move = "WHITE"
        self.parent.w_pawn0.set(1,0)
        self.parent.w_pawn0.makeVisible()
        self.parent.w_pawn1.set(1,1)
        self.parent.w_pawn1.makeVisible()
        self.parent.w_pawn2.set(1,2)
        self.parent.w_pawn2.makeVisible()
        self.parent.w_pawn3.set(1,3)
        self.parent.w_pawn3.makeVisible()
        self.parent.w_pawn4.set(1,4)
        self.parent.w_pawn4.makeVisible()
        self.parent.w_pawn5.set(1,5)
        self.parent.w_pawn5.makeVisible()
        self.parent.w_pawn6.set(1,6)
        self.parent.w_pawn6.makeVisible()
        self.parent.w_pawn7.set(1,7)
        self.parent.w_pawn7.makeVisible()

        self.parent.w_knight1.set(0,1)
        self.parent.w_knight1.makeVisible()
        self.parent.w_knight2.set(0,6)
        self.parent.w_knight2.makeVisible()

        self.parent.w_bishop1.set(0,2)
        self.parent.w_bishop1.makeVisible()
        self.parent.w_bishop2.set(0,5)
        self.parent.w_bishop2.makeVisible()

        self.parent.w_rook1.set(0,0)
        self.parent.w_rook1.makeVisible()
        self.parent.w_rook2.set(0,7)
        self.parent.w_rook2.makeVisible()

        self.parent.w_queen1.set(0,3)
        self.parent.w_queen1.makeVisible()

        self.parent.w_king1.set(0,4)
        self.parent.w_king1.makeVisible()

        self.parent.b_pawn0.set(6,0)
        self.parent.b_pawn0.makeVisible()
        self.parent.b_pawn1.set(6,1)
        self.parent.b_pawn1.makeVisible()
        self.parent.b_pawn2.set(6,2)
        self.parent.b_pawn2.makeVisible()
        self.parent.b_pawn3.set(6,3)
        self.parent.b_pawn3.makeVisible()
        self.parent.b_pawn4.set(6,4)
        self.parent.b_pawn4.makeVisible()
        self.parent.b_pawn5.set(6,5)
        self.parent.b_pawn5.makeVisible()
        self.parent.b_pawn6.set(6,6)
        self.parent.b_pawn6.makeVisible()
        self.parent.b_pawn7.set(6,7)
        self.parent.b_pawn7.makeVisible()

        self.parent.b_knight1.set(7,1)
        self.parent.b_knight1.makeVisible()
        self.parent.b_knight2.set(7,6)
        self.parent.b_knight2.makeVisible()

        self.parent.b_bishop1.set(7,2)
        self.parent.b_bishop1.makeVisible()
        self.parent.b_bishop2.set(7,5)
        self.parent.b_bishop2.makeVisible()

        self.parent.b_rook1.set(7,0)
        self.parent.b_rook1.makeVisible()
        self.parent.b_rook2.set(7,7)
        self.parent.b_rook2.makeVisible()

        self.parent.b_queen1.set(7,3)
        self.parent.b_queen1.makeVisible()

        self.parent.b_king1.set(7,4)
        self.parent.b_king1.makeVisible()

    def square_pos(self,x,y):
        square_size = self.width/8
        return (math.trunc(y/square_size),math.trunc(x/square_size),math.trunc(y/square_size)*8+math.trunc(x/square_size))

    def legal_move(self, down, up):
        if self.current_move == self.color[down[2]] and up[2] in self.generate_moves(down):
            return True;
        else:
            return False;

    def current_move_swap(self):
        self.move += 1
        if self.current_move == "WHITE":
            self.current_move = "BLACK"
        elif self.current_move == "BLACK":
            self.current_move = "WHITE"

class Knight(Widget):
    position_row = NumericProperty(-1)
    position_col = NumericProperty(-1)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = NumericProperty(0)
    first = True

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"
    
    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        self.position_col = col
        self.position_row = row

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        
        temp_pos = self.position_row*8+self.position_col

        self.parent.names[self.position_row*8+self.position_col] = self
        self.parent.piece[self.position_row*8+self.position_col] = "KNIGHT"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"
        self.first = False
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "KNIGHT"
    pass

class Bishop(Widget):
    position_row = NumericProperty(-1)
    position_col = NumericProperty(-1)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = NumericProperty(0)
    first = True

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"
    
    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        self.first = False
        self.position_col = col
        self.position_row = row

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        
        temp_pos = self.position_row*8+self.position_col

        self.parent.names[self.position_row*8+self.position_col] = self
        self.parent.piece[self.position_row*8+self.position_col] = "BISHOP"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "BISHOP"
    pass

class Rook(Widget):
    position_row = NumericProperty(-1)
    position_col = NumericProperty(-1)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = NumericProperty(0)
    castleable = ObjectProperty(True)
    first = True

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"
    
    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if (self.parent.move == 0):
            self.castleable = True
        else:
            self.castleable = False
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        self.position_col = col
        self.position_row = row

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        
        temp_pos = self.position_row*8+self.position_col
        
        self.parent.names[self.position_row*8+self.position_col] = self
        self.parent.piece[self.position_row*8+self.position_col] = "ROOK"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"

        self.first = False
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "ROOK"
    pass

class Queen(Widget):
    position_row = NumericProperty(-1)
    position_col = NumericProperty(-1)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = NumericProperty(0)
    first = True

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"
    
    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        self.position_col = col
        self.position_row = row

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        
        temp_pos = self.position_row*8+self.position_col
        
        self.parent.names[self.position_row*8+self.position_col] = self
        self.parent.piece[self.position_row*8+self.position_col] = "QUEEN"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"

        self.first = False
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "QUEEN"
    pass

class King(Widget):
    position_row = NumericProperty(-1)
    position_col = NumericProperty(-1)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = NumericProperty(0)
    castleable = ObjectProperty(True)
    first = True

    def inCheck(self):
        color = self.parent.color
        piece = self.parent.piece
        names = self.parent.names

        king_row = self.position_row
        king_col = self.position_col

        # From above check
        if king_row < 7:
            temp_row = king_row+1
            temp_pos = temp_row*8+king_col
            while temp_row < 7 and piece[temp_pos] == "EMPTY":
                temp_row+=1;
                temp_pos+=8;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From front: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "ROOK" or hit_p == "QUEEN"):
                    print("In check")

        # From below check
        if king_row > 0:
            temp_row = king_row-1
            temp_pos = temp_row*8+king_col
            while temp_row > 0 and piece[temp_pos] == "EMPTY":
                temp_row-=1;
                temp_pos-=8;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From back: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "ROOK" or hit_p == "QUEEN"):
                    print("In check")

        # From right check
        if king_col < 7:
            temp_col = king_col+1
            temp_pos = king_row*8+temp_col
            while temp_col < 7 and piece[temp_pos] == "EMPTY":
                temp_col+=1;
                temp_pos+=1;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From right: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "ROOK" or hit_p == "QUEEN"):
                    print("In check")

        # From left check
        if king_col > 0:
            temp_col = king_col-1
            temp_pos = king_row*8+temp_col
            while temp_col > 0 and piece[temp_pos] == "EMPTY":
                temp_col-=1;
                temp_pos-=1;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From left: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "ROOK" or hit_p == "QUEEN"):
                    print("In check")

        # From diagonal top right check
        if king_row < 7 and king_col < 7:
            temp_count = 1
            temp_row = king_row+1
            temp_col = king_col+1
            temp_pos = temp_row*8+temp_col
            while temp_col < 7 and temp_row < 7 and piece[temp_pos] == "EMPTY":
                temp_col+=1;
                temp_row+=1;
                temp_pos+=9;
                temp_count += 1
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From upper right: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "BISHOP" or hit_p == "QUEEN"):
                    print("In check")
                elif (temp_count == 1 and (hit_p == "PAWN" or hit_p == "KING") and self.parent.forward != hit_c):
                    print("Pawn Check")

        # From diagonal top left check
        if king_row < 7 and king_col > 0:
            temp_count = 0
            temp_row = king_row+1
            temp_col = king_col-1
            temp_pos = temp_row*8+temp_col
            while temp_col > 0 and temp_row < 7 and piece[temp_pos] == "EMPTY":
                temp_col-=1;
                temp_row+=1;
                temp_pos+=7;
                temp_count+=1
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From upper left: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "BISHOP" or hit_p == "QUEEN"):
                    print("In check")
                elif (temp_count == 1 and (hit_p == "PAWN" or hit_p == "KING") and self.parent.forward == hit_c):
                    print("Pawn Check")

        # From diagonal bottom right check
        if king_row > 0 and king_col < 7:
            temp_row = king_row-1
            temp_col = king_col+1
            temp_pos = temp_row*8+temp_col
            while temp_col < 7 and temp_row > 0 and piece[temp_pos] == "EMPTY":
                temp_col+=1;
                temp_row-=1;
                temp_pos-=7;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From lower right: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "BISHOP" or hit_p == "QUEEN"):
                    print("In check")
                elif (temp_count == 1 and (hit_p == "PAWN" or hit_p == "KING") and self.parent.forward != hit_c):
                    print("Pawn Check")

        # From diagonal bottom left check
        if king_row > 0 and king_col > 0:
            temp_row = king_row-1
            temp_col = king_col-1
            temp_pos = temp_row*8+temp_col
            while temp_col > 0 and temp_row > 0 and piece[temp_pos] == "EMPTY":
                temp_col-=1;
                temp_row-=1;
                temp_pos-=9;
            hit_p = piece[temp_pos]
            hit_c = color[temp_pos]
            print("From lower left: ",hit_c, hit_p)
            if (hit_c == "BLACK" and self.white == 1) or (hit_c == "WHITE" and self.white == 0):
                if (hit_p == "BISHOP" or hit_p == "QUEEN"):
                    print("In check")
                elif (temp_count == 1 and (hit_p == "PAWN" or hit_p == "KING") and self.parent.forward != hit_c):
                    print("Pawn Check")
        # Knight checks
        if self.white == 1:
            temp_c = "WHITE"
        else:
            temp_c = "BLACK"
        if king_row < 7 and king_col > 1:
            temp_col=king_col-2
            temp_row=king_row+1
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row < 7 and king_col < 6:
            temp_col=king_col+2
            temp_row=king_row+1
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row > 0 and king_col > 1:
            temp_col=king_col-2
            temp_row=king_row-1
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row > 0 and king_col < 6:
            temp_col=king_col+2
            temp_row=king_row-1
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row > 1 and king_col < 7:
            temp_col=king_col+1
            temp_row=king_row-2
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row > 1 and king_col > 0:
            temp_col=king_col-1
            temp_row=king_row-2
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row < 6 and king_col > 0:
            temp_col=king_col-1
            temp_row=king_row+2
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

        if king_row < 6 and king_col < 7:
            temp_col=king_col+1
            temp_row=king_row+2
            temp_pos = temp_row*8+temp_col
            if piece[temp_pos] == "KNIGHT" and color[temp_pos] != temp_c:
                print("Check dectected, knight at ", temp_pos)

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"
    
    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        if self.position_col == 4 and col == 2:
            if (self.white == 1 and self.parent.forward == "WHITE") or (self.white == 0 and self.parent.forward == "BLACK"): 
                self.parent.names[0].set(0,3)
            else:
                self.parent.names[56].set(7,3)
        elif self.position_col == 4 and col == 6:
            if (self.white == 1 and self.parent.forward == "WHITE") or (self.white == 0 and self.parent.forward == "BLACK"): 
                self.parent.names[7].set(0,5)
            else:
                self.parent.names[56].set(7,5)

        self.position_col = col
        self.position_row = row

        if self.parent.move == 0:
            self.castleable = True
        else:
            self.castleable = False

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        
        temp_pos = self.position_row*8+self.position_col
        
        self.parent.names[self.position_row*8+self.position_col] = self
        self.parent.piece[self.position_row*8+self.position_col] = "KING"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"

        self.first = False
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "KING"
    pass

class Pawn(Widget):
    position_row = NumericProperty(0)
    position_col = NumericProperty(0)
    white = NumericProperty(1)
    visible = NumericProperty(0)
    p_size = ObjectProperty(0)
    en_passantable = ObjectProperty(False)
    en_passantable_move = -1
    first = True

    def makeVisible(self):
        self.visible = 1
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white == 1 else "BLACK"

    def makeNotVisible(self):
        self.visible = 0
        if self.parent.color[self.position_row*8+self.position_col] == "WHITE":
            self.parent.black_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        if self.parent.color[self.position_row*8+self.position_col] == "BLACK":
            self.parent.white_capture.append(self.parent.names[self.position_row*8+self.position_col]) 
        self.parent.color[self.position_row*8+self.position_col] = "EMPTY"
        self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"

    def set(self, row, col):
        if not self.first:
            self.parent.names[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.piece[self.position_row*8+self.position_col] = "EMPTY"
            self.parent.color[self.position_row*8+self.position_col] = "EMPTY"

        if abs(self.position_row - row) == 2:
            self.en_passantable = True
            self.en_passantable_move = (self.parent.move+1)
        else:
            self.en_passantable = False

        diag_move = True if self.position_col != col else False

        self.position_col = col
        self.position_row = row
        
        temp_pos = self.position_row*8+self.position_col

        if (self.parent.piece[self.position_row*8+self.position_col]) != "EMPTY":
            self.parent.names[self.position_row*8+self.position_col].makeNotVisible()
        if (diag_move and self.parent.piece[temp_pos-8] == "PAWN" and self.parent.names[temp_pos-8].en_passantable_move == self.parent.move):
            self.parent.names[temp_pos-8].makeNotVisible()
        if (diag_move and self.parent.piece[temp_pos+8] == "PAWN" and self.parent.names[temp_pos+8].en_passantable_move == self.parent.move):
            self.parent.names[temp_pos+8].makeNotVisible()
        self.parent.names[self.position_row*8+self.position_col] = self
        
        self.parent.piece[self.position_row*8+self.position_col] = "PAWN"
        self.parent.color[self.position_row*8+self.position_col] = "WHITE" if self.white else "BLACK"

        self.first = False
        if self.visible == 1:
            self.parent.color[row*8+col] = "WHITE" if self.white == 1 else "BLACK"
            self.parent.piece[row*8+col] = "PAWN"
    pass

class Marker(Widget):
    position_row = NumericProperty(0)
    position_col = NumericProperty(0)
    p_size = NumericProperty(0)
    visible = 1

    def markSpace(self, row, col):
        self.position_row = row
        self.position_col = col

class ChessApp(App):
    def build(self):
        return ChessGame()

if __name__ == '__main__':
    g_size = 0
    ChessApp().run()

