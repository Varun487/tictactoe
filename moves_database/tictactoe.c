#include <stdio.h>
#include <stdlib.h>

struct grid
{
    char char_board[9]; // contains the current characters of the board in respective positions
    int control_board[9]; // has truth values of respective positions
};

// ------------------------  DECLARATIONS ------------------------------------

// to display the board in a readable form
void display(struct grid* board);

// move function
int move(struct grid* board,int * win,int * tie,int move_num,int bytes_per_num[],int char_per_line[],int moves_ledger[],char filename[]);

// -----------------------------  MAIN  ----------------------------------------

int main()
{
    // WELCOME MESSAGE
    printf("\n\t\t\tWELCOME TO TICTACTOE\t\n\n");
    printf("PLEASE ENTER THE NUMBER REPRESENTING THE CORRESPONDING POSTION IN THE BOARD AS INPUT\n");
    // iniitializing the tictactoe board
    struct grid board = {"OOOOOOOOO",{0}};
    int i,win = 0,tie = 0,bytes_per_num[]={0,81,891,9477},char_per_line[]={7,9,11,13},moves_ledger[4] = {0};
    display(&board);
    // first move
    move(&board,&win,&tie,1,bytes_per_num,char_per_line,moves_ledger,"first_move.txt");
    // second move
    move(&board,&win,&tie,2,bytes_per_num,char_per_line,moves_ledger,"second_move.txt");
    // third move
    move(&board,&win,&tie,3,bytes_per_num,char_per_line,moves_ledger,"third_move.txt");
    if(!(win || tie))
    {
        move(&board,&win,&tie,4,bytes_per_num,char_per_line,moves_ledger,"fourth_move.txt");
    }
    if(win)
    {
        for(i=0;i<9;i++)
        {
            if(!(board.control_board[i]))
            {
                board.control_board[i] = 1;
                board.char_board[i] = ' ';
            }
        }
        printf("\n -----------------------------  FINAL BOARD  ----------------------------------------\n");
        display(&board);
        printf("\n\t\t\tCOMPUTER PLAYER WINS\n");
    }
    else
    {
        for(i=0;i<9;i++)
        {
            if(!(board.control_board[i]))
            {
                board.control_board[i] = 1;
                board.char_board[i] = 'O';
            }
        }
        printf("\n -----------------------------  FINAL BOARD  ----------------------------------------\n");
        display(&board);
        printf("\n\t\t\tGAME ENDS IN TIE\n");
    }
    return 0;
}

// ------------------------  FUNCTION DEFINITIONS ------------------------------------

// to display the board in a readable form
void display(struct grid* board)
{
    int i;
    for (i=0;i<9;i++)
    {
        // goes to next line if multiple of 3
        if (i%3 == 0)
        {
            printf("\n");
        }
        if (board->control_board[i])
        {
            printf(" \'%c\' ",board->char_board[i]);
        }
        else
        {
            printf("  %d  ",i+1);
        }
    }
    printf("\n");
}

// takes user input, finds computer move in file, makes corresponding changes to the board
int move(struct grid* board,int * win,int * tie,int move_num,int bytes_per_num[],int char_per_line[],int moves_ledger[],char filename[])
{
    char compmove;
    int inp,valid = 1;
    long offset;
    FILE *fp;
    fp = fopen(filename, "r"); // opens given file in read mode
    // to get a valid input
    while (valid)
    {
        printf("\nEnter your move: ");scanf("%d",&inp);
        if (inp > 9 || inp < 1 || board->control_board[inp-1])
        {
            printf("\nInvalid input.\n");
        }
        else
        {
            moves_ledger[move_num - 1] = inp;
            valid = 0;
        }
    }
    // calculating offset for comp move
    offset = (bytes_per_num[move_num - 1]*(moves_ledger[move_num-2]-1))+(char_per_line[move_num - 1]*moves_ledger[move_num - 1] - 5);
    if (move_num == 3)
    {
        offset = (bytes_per_num[move_num - 1]*(moves_ledger[move_num-3]-1)) + (99*(moves_ledger[move_num - 2]-1)) + (char_per_line[move_num - 1]*moves_ledger[move_num - 1] - 5);
    }
    if (move_num == 4)
    {
        offset = (9477*(moves_ledger[move_num-4]-1)) + (1053*(moves_ledger[move_num-3]-1)) + (117*(moves_ledger[move_num-2]-1)) + (char_per_line[move_num - 1]*moves_ledger[move_num - 1] - 5);
    }
    // to find the computer's move
    fseek(fp,offset,0);
    compmove = getc(fp);
    if (move_num == 3 || move_num == 4)
    {
        fseek(fp,offset+2,0);
        if (getc(fp) == 't')
        {
            *tie = 1;
        }
        fseek(fp,offset+2,0);
        if (getc(fp) == 'w')
        {
            *win = 1;
        }
    }
    // informing user of moves made
    printf("\nThe User move (\'O\') is %d, computer response (\'X\') is %c\n",inp,compmove);
    // changing board according to user move
    board->control_board[inp - 1] = 1;
    board->char_board[inp - 1] = 'O';
    // changing board according to computer move
    int comp_index = compmove-'0';
    board->control_board[comp_index - 1] = 1;
    board->char_board[comp_index - 1] = 'X';
    fclose(fp);
    display(board);
    return 0;
}