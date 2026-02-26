from Game_class import Case

def test_activer_clears_transparency():
    c = Case(0, 0)
    
    # 1. Make it transparent (Ghost)
    c.act_transp()
    print(f"After act_transp: Transparent={c.transparent}, Color={c.coul_case}")
    
    # 2. Activate it (Piece lands on it)
    # This simulates what happens in hard_drop or bouger_piece
    c.activer('#FF0000') # Red
    print(f"After activer: Transparent={c.transparent}, Color={c.coul_case}")
    
    # 3. Simulate update_gui clearing old ghosts
    # If transparent is still True, it will be cleared to Black
    if c.transparent:
        print("Bug Detected! Cell is still transparent. It would be cleared to black in the next frame.")
        c.des_transp('#161614')
        print(f"After ghost cleanup: Color={c.coul_case}")
    else:
        print("Cell is NOT transparent. Color preserved.")

if __name__ == "__main__":
    test_activer_clears_transparency()
