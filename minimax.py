from copy import deepcopy

def minimax(board,depth,depth_limit):
    best_board=None
    current_depth=depth+1

    if current_depth==depth_limit:
        return board,board.evaluate_board_desiarbility()

    if board.turn==1:
        best_score=float('-inf')
        piece,move,turn=board.first_two_moves_picker()
        best_board=deepcopy(board)
        best_board.move_piece(str(piece.x)+str(piece.y),move)

    if board.turn==2:
        best_score=float('inf')
        piece,move,turn=board.first_two_moves_picker()
        best_board=deepcopy(board)
        best_board.move_piece(str(piece.x)+str(piece.y),move)



    elif board.turn%2==1 and board.turn != 1 and board.turn != 2:
        best_score=float('-inf')
        print('ada')
        for piece,move in board.expand_black_moves():

            print(type(move))
            print(move[0])
            best_board=deepcopy(board)
            best_board.move_piece(str(piece.x)+str(piece.y),move[1])
            minimax_board,minimax_returned_score = minimax(best_board,current_depth,depth_limit)
            print(minimax_returned_score,minimax_board.turn)
            print("gggggggggggg")

            if minimax_returned_score > best_score:
                print(minimax_returned_score,minimax_board.turn)
                best_board=minimax_board
                best_score=minimax_returned_score

    else:
        best_score=float('inf')
        minimax_board,minimax_returned_score= minimax(best_board,current_depth,depth_limit)
        if minimax_returned_score < best_score:
            best_board=minimax_board
            best_score=minimax_returned_score

    return best_board,best_score

