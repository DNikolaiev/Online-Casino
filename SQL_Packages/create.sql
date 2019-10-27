/* CREATING TABLES */
create table "USER" 
(
   USER_NAME            VARCHAR2(20),
   USER_AGE             NUMBER,
   USER_EMAIL           VARCHAR2(20)         not null,
   USER_LOGIN           VARCHAR2(20)         not null,
   USER_PASSWORD        VARCHAR2(20),
   constraint PK_USER primary key (USER_LOGIN)
);
create table BANKINFO 
(
   USER_LOGIN           VARCHAR2(20)         not null,
   BANKINFO_CARD_NUMBER NUMBER(16)           not null,
   BANKINFO_EXPIRATION_DATE DATE                 not null,
   BANKINFO_ADRESS      VARCHAR2(30),
   constraint PK_BANKINFO primary key (USER_LOGIN, BANKINFO_CARD_NUMBER)
);
alter table BANKINFO
   add constraint FK_BANKINFO_USER_BANK_USER foreign key (USER_LOGIN)
      references "USER" (USER_LOGIN);
      
create table BET 
(
   BET_MONEY            FLOAT(6),
   BET_MULTIPLIER       NUMBER(2),
   BET_ID               INTEGER              not null,
   BET_DATE             DATE                 not null,
   BET_NAME             VARCHAR2(30)         not null,
   constraint PK_BET primary key (BET_ID)
);
ALTER TABLE BET ADD DELETED DATE DEFAULT NULL;
create table Casino 
(
   BET_ID               INTEGER              not null,
   USER_LOGIN           VARCHAR2(20)         not null,
   constraint PK_CASINO primary key (BET_ID, USER_LOGIN)
);
alter table Casino
   add constraint FK_CASINO_BET foreign key (BET_ID)
      references BET (BET_ID);

alter table Casino
   add constraint FK_CASINO_USER foreign key (USER_LOGIN)
      references "USER" (USER_LOGIN);
Alter Table Casino ADD BET_DATE DATE not null;
Alter Table "USER" ADD USER_MONEY float  default '0';

create OR REPLACE view bet_view as
Select BET_ID, BET_MONEY, BET_MULTIPLIER, BET_NAME, BET_DATE, DELETED FROM BET;

/* CHECK AND REGEXP */
Alter Table "USER" ADD CONSTRAINT user_name_check CHECK (REGEXP_LIKE(USER_NAME, '^[A-Z]{1,1}[a-z]{2,29}$'));
Alter Table "USER" ADD CONSTRAINT user_email_unique UNIQUE (USER_EMAIL);
Alter Table "USER" ADD CONSTRAINT user_age_check CHECK (REGEXP_LIKE(USER_AGE, '^[[:digit:]]{1,3}'));
Alter Table "USER" ADD CONSTRAINT user_login_check CHECK (REGEXP_LIKE(USER_LOGIN, '^[A-Z]{1,1}[a-z]{0,29}$'));
Alter Table "USER" ADD CONSTRAINT user_pass_check CHECK (REGEXP_LIKE(USER_PASSWORD, '^[a-zA-Z0-9]{4,}$'));


Alter Table "BET" ADD CONSTRAINT bet_money_check CHECK (REGEXP_LIKE(BET_MONEY, '^[[:digit:]]{1,6}'));
Alter Table "BET" ADD CONSTRAINT bet_multiplier_check CHECK (REGEXP_LIKE(BET_MULTIPLIER, '^[[:digit:]]{1,2}'));
Alter Table "BET" ADD CONSTRAINT bet_id_check CHECK (REGEXP_LIKE(BET_ID, '^[[:digit:]]{1,3}'));

Alter Table "BANKINFO" ADD CONSTRAINT bankInfo_cardNumber_check CHECK (REGEXP_LIKE(BANKINFO_CARD_NUMBER, '^[[:digit:]]{16}'));
Alter Table "BANKINFO" ADD CONSTRAINT bankInfo_user_login_check CHECK (REGEXP_LIKE(USER_LOGIN, '^[A-Z]{1,1}[a-z]{0,29}$'));

Alter Table "CASINO" ADD CONSTRAINT casino_user_login_check CHECK (REGEXP_LIKE(USER_LOGIN, '^[A-Z]{1,1}[a-z]{0,29}$'));
Alter Table "CASINO" ADD CONSTRAINT casino_bet_id_check CHECK (REGEXP_LIKE(BET_ID, '^[[:digit:]]{1,4}'));
