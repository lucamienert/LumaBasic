class Types:
    STATE_NORMAL = 0
    STATE_HALT = 1
    STATE_GOTO = 3
    STATE_LOOP_START = 4
    STATE_LOOP_NORMAL = 5
    STATE_LOOP_DONE = 6
    STATE_GOSUB = 7
    STATE_RETURN = 8

    TT_STRING = 0
    TT_UINT = 1
    TT_UFLOAT = 2
    TT_IDENTIFIER = 3

    KW_ABS = 10   
    KW_AND = 11   
    KW_ASC = 12   
    KW_ATN = 13   
    KW_CHR = 14   
    KW_COS = 15   
    KW_DATA = 16  
    KW_DIM = 17   
    KW_ELSE = 18  
    KW_END = 19   
    KW_EXP = 20   
    KW_FOR = 21   
    KW_GOSUB = 22 
    KW_GOTO = 23  
    KW_IF = 24    
    KW_INPUT = 25 
    KW_INT = 26   
    KW_LEFT = 27  
    KW_LEN = 28   
    KW_LET = 29   
    KW_LOG = 30   
    KW_MID = 31   
    KW_NEXT = 32  
    KW_NOT = 33   
    KW_ON = 34    
    KW_OR = 35    
    KW_SYSOUT = 36 
    KW_READ = 37  
    KW_REM = 38   
    KW_RETURN = 39
    KW_RIGHT = 40 
    KW_RND = 41   
    KW_SGN = 42   
    KW_SIN = 43   
    KW_SPC = 44   
    KW_SQR = 45   
    KW_STEP = 46  
    KW_STR = 47   
    KW_TAN = 48   
    KW_THEN = 49  
    KW_TO = 50    
    KW_XOR = 51   

    SYM_ADD = 70
    SYM_SUB = 71
    SYM_MUL = 72
    SYM_DIV = 73
    SYM_MOD = 74
    SYM_LT = 75
    SYM_GT = 76
    SYM_LE = 77
    SYM_GE = 78
    SYM_NE = 79
    SYM_EQ = 80
    SYM_LPAREN = 81
    SYM_RPAREN = 82
    SYM_COMMA = 83
    SYM_COLON = 84
    SYM_SEMICOLON = 85
    SYM_NEWLINE = 86

    KEYWORDS = {
        'ABS':  KW_ABS, 
        'AND': KW_AND, 
        'ASC': KW_ASC, 
        'ATN': KW_ATN,
        'CHR': KW_CHR, 
        'COS': KW_COS, 
        'DATA': KW_DATA, 
        'DIM': KW_DIM,
        'END':  KW_END, 
        'EXP': KW_EXP, 
        'FOR': KW_FOR, 
        'GOSUB': KW_GOSUB,
        'GOTO': KW_GOTO, 
        'IF':  KW_IF, 
        'INPUT': KW_INPUT, 
        'INT': KW_INT,
        'LEFT': KW_LEFT, 
        'LEN': KW_LEN, 
        'LET': KW_LET, 
        'LOG': KW_LOG,
        'MID': KW_MID, 
        'NEXT': KW_NEXT, 
        'NOT': KW_NOT, 
        'ON': KW_ON,
        'OR': KW_OR, 
        'SYSOUT': KW_SYSOUT, 
        'READ': KW_READ, 
        'REM': KW_REM,
        'RETURN': KW_RETURN, 
        'RIGHT': KW_RIGHT, 
        'RND': KW_RND, 
        'SGN': KW_SGN,
        'SIN': KW_SIN, 
        'SPC': KW_SPC, 
        'SQR': KW_SQR, 
        'STEP': KW_STEP,
        'STR': KW_STR, 
        'TAN': KW_TAN, 
        'THEN': KW_THEN, 
        'TO': KW_TO,
        'XOR': KW_XOR
    }

    SYMBOLS = {
        '+': SYM_ADD, 
        '-': SYM_SUB, 
        '*': SYM_MUL, 
        '/': SYM_DIV,
        '%': SYM_MOD, 
        '<': SYM_LT, 
        '>': SYM_GT, 
        '<=': SYM_LE,
        '>=': SYM_GE, 
        '<>': SYM_NE, 
        '=': SYM_EQ, 
        '(': SYM_LPAREN,
        ')': SYM_RPAREN, 
        ',': SYM_COMMA, 
        ':': SYM_COLON, 
        ';': SYM_SEMICOLON,
        '\n': SYM_NEWLINE
    }