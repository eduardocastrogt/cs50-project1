--Crypto module
create extension pgcrypto;

--Table for register the user information
create table Tbl_User
(
    Id_User serial primary key, --Id_user is autoincrement
    Name varchar(50) not null,
    LastName varchar(50) not null,
    Email varchar(75) not null unique,
    Pass text not null --will be crypt
);

--drop table tbl_book
create table Tbl_Book
(
    Id_Book serial primary key,
    ISBN text not null,
    Title text not null,
    Author text not null,
    Year int not null
);

drop table Tbl_Review
create table Tbl_Review
(
    Id_Review serial primary key,
    Id_user int not null references Tbl_User(Id_User),
    ISBN text not null,
    Comment text not null,
    Count_review int not null,
    Register timestamp not null,
    unique(Id_User, ISBN)

);

--Function for store User information 
create or replace function Book_SaveUser (name_user varchar(50), lastname_user varchar(50), email_user varchar(75), pass_user text) returns void as $$
    begin
        insert into Tbl_User(Name, LastName, Email, Pass)
        values (upper(name_user), upper(lastname_user), lower(email_user), crypt(pass_user, gen_salt('bf')));
    end
$$ language plpgsql;

--Function ExistUser (for login)
create or replace function Book_ExistUser (email_user varchar(75), user_password text) returns table(user_id int, user_name text) as $$
        select
            Id_user as user_id,-- into user
            Name || ' ' || LastName as user_name
        from
            Tbl_User
        where
            Email = email_user
            and Pass = crypt(user_password, Pass);
$$ language sql

--Function Search Book
create or replace function Search_Book (search_ text) returns Tbl_book as $$
begin
    return QUERY select
        *
    from
        Tbl_book
    where
        isbn like search_--like '%' ||  search_ || '%'
        or title like search_ --like '%' ||  search_ || '%'
        or author like search_ --like '%' ||  search_ || '%'
end;
$$ language sql
