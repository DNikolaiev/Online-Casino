CREATE OR REPLACE PACKAGE USERPACKAGE IS
TYPE USER_DATA IS RECORD (USERLOGIN VARCHAR2(60), USERNAME  VARCHAR2(60), USERAGE NUMBER(4), USERMAIL VARCHAR2(60),USERMONEY FLOAT(60)); 
TYPE TBLUSERDATA IS TABLE OF USER_DATA;
FUNCTION GET_USER(USERLOG IN VARCHAR2) RETURN TBLUSERDATA PIPELINED;
FUNCTION LOGIN(LOGVAR IN VARCHAR2, PASSVAR IN VARCHAR2) RETURN VARCHAR2;
FUNCTION REGISTRATE(LOGIN IN VARCHAR2, PASS IN VARCHAR2, EMAIL IN VARCHAR2, AGE IN VARCHAR2, NAMEVAR IN VARCHAR2) RETURN VARCHAR2;
PROCEDURE CHANGE_PLAYER_BALANCE (USERLOGIN IN VARCHAR2 , AMOUNT IN FLOAT);
FUNCTION SHOW_USER_MONEY(USERLOGIN IN VARCHAR2) RETURN FLOAT;
END USERPACKAGE;
/
CREATE OR REPLACE PACKAGE BODY USERPACKAGE IS
FUNCTION GET_USER(USERLOG IN VARCHAR2) RETURN TBLUSERDATA PIPELINED
IS
BEGIN
    FOR CURR IN (
    SELECT USER_LOGIN,USER_NAME,USER_AGE,USER_EMAIL,USER_MONEY FROM "USER" WHERE USER_LOGIN=USERLOG
    ) LOOP
        PIPE ROW (CURR);
    END LOOP;
END GET_USER;
FUNCTION SHOW_USER_MONEY(USERLOGIN IN VARCHAR2) RETURN FLOAT IS
MONEY FLOAT;
BEGIN
    SELECT USER_MONEY INTO MONEY FROM "USER" WHERE USER_LOGIN=USERLOGIN;
    RETURN MONEY;
END SHOW_USER_MONEY;
FUNCTION LOGIN(LOGVAR IN VARCHAR2, PASSVAR IN VARCHAR2) RETURN VARCHAR2 AS
    MATCH_COUNT NUMBER(2):=0;
    BEGIN
    SELECT COUNT(*) INTO MATCH_COUNT FROM "USER"
    WHERE USER_LOGIN=LOGVAR AND USER_PASSWORD=PASSVAR;
    IF MATCH_COUNT=0 THEN RETURN 'FALSE';
    ELSIF MATCH_COUNT=1 THEN RETURN 'TRUE';
    ELSE RETURN 'ERROR';
    END IF;
END LOGIN;
FUNCTION REGISTRATE(LOGIN IN VARCHAR2, PASS IN VARCHAR2, EMAIL IN VARCHAR2, AGE IN VARCHAR2, NAMEVAR IN VARCHAR2) RETURN VARCHAR2 IS
    counter number;
    mailCounter number;
    
    BEGIN
    Select COUNT( user_login ) into counter from "USER" where user_login=LOGIN;
    Select COUNT( user_email ) into mailCounter from "USER" where user_email=EMAIL;
    if counter >= 1 or mailCounter >=1 then
    dbms_output.put_line('Already Exists'); 
    RETURN 'FALSE';
    else
    INSERT INTO "USER" (USER_LOGIN, USER_PASSWORD, USER_EMAIL, USER_AGE, USER_NAME) VALUES (LOGIN, PASS, EMAIL, AGE, NAMEVAR);
    RETURN 'TRUE';
    end if;
    EXCEPTION 
    WHEN OTHERS THEN RETURN 'FALSE';
END REGISTRATE;
PROCEDURE CHANGE_PLAYER_BALANCE (USERLOGIN IN VARCHAR2, AMOUNT IN FLOAT) IS
testVar FLOAT;
BEGIN
    if AMOUNT < 0 THEN
        Select USER_MONEY into testVar from "USER" where user_login=USERLOGIN;
        if testVar + AMOUNT <= 0 THEN
        Update "USER" SET USER_MONEY = 0 WHERE USER_LOGIN=USERLOGIN;
        RETURN;
        END IF;
    end if;
    UPDATE "USER" SET USER_MONEY=USER_MONEY+AMOUNT WHERE USER_LOGIN=USERLOGIN;
END CHANGE_PLAYER_BALANCE;
END USERPACKAGE;
