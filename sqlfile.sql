create database TVTS;
SET SQL_SAFE_UPDATES = 0;
create table TTTS(
	id int not null primary key auto_increment,
    hovaten nvarchar(255) not null,
    sdt varchar(15) not null,
    cauhoi text not null,
    cautraloi text not null,
    thoigianhoi datetime not null default current_timestamp()
);
insert into TTTS (hovaten, sdt, cauhoi, cautraloi) values ('nguyễn mạnh quốc khang', '0973636954', 'ngày học', 'ngày mai');
insert into TTTS (hovaten, sdt, cauhoi, cautraloi) values ('nguyễn lam trường', '0973636954', 'ngày học', 'ngày mai');
select hovaten, sdt, cauhoi, cautraloi, thadminsoigianhoi from TTTS;
select distinct cauhoi, cautraloi from TTTS where cauhoi not like 'Hệ thống chưa nhận diện được giọng nói của bạn xin hãy thử lại!' or cautraloi != 'Trợ lý không hiểu, xin thử lại!' ORDER BY cauhoi, cautraloi;
select distinct cauhoi, cautraloi from TTTS 
where cauhoi not like 'Hệ thống chưa nhận diện được giọng nói của bạn xin hãy thử lại!'
having cautraloi != 'Trợ lý không hiểu, xin thử lại!'  
ORDER BY cauhoi, cautraloi;
select distinct cauhoi, cautraloi from TTTS where cautraloi not like 'Trợ lý không hiểu, xin thử lại!' or cautraloi not like 'ngày mai' ;
select distinct cauhoi from TTTS where cauhoi not like 'Hệ thống chưa nhận diện được giọng nói của bạn xin hãy thử lại!';
DELETE FROM TTTS;
drop table ttts;

create table Chung(
	id int not null primary key auto_increment,
    macauhoi nvarchar(255) not null,
    cauhoi text not null,
    cautraloi text not null,
    thoigiancapnhat datetime not null default current_timestamp()
);
insert into Chung (macauhoi, cauhoi, cautraloi) values ('C01','ngày học', 'ngày mai');
select id, macauhoi, cauhoi, cautraloi, thoigiancapnhat from Chung;
update Chung set macauhoi = 'C02', cauhoi = 'tiền học', cautraloi = 'free', thoigiancapnhat = now() where id = 2;
DELETE FROM Chung where id = 7;
select * from Chung;
SELECT id, macauhoi, cauhoi, cautraloi, thoigiancapnhat FROM chung where macauhoi LIKE '%C01%' or cauhoi LIKE '%n%';

create table CNTT(
	id int not null primary key auto_increment,
    macauhoi nvarchar(255) not null,
    cauhoi text not null,
    cautraloi text not null,
    thoigiancapnhat datetime not null default current_timestamp()
);
insert into cntt (macauhoi, cauhoi, cautraloi) values ('C01','ngày học', 'ngày mai');
select id, macauhoi, cauhoi, cautraloi, thoigiancapnhat from cntt;

create table QTKD(
	id int not null primary key auto_increment,
    macauhoi nvarchar(255) not null,
    cauhoi text not null,
    cautraloi text not null,
    thoigiancapnhat datetime not null default current_timestamp()
);

create table DLICH(
	id int not null primary key auto_increment,
    macauhoi nvarchar(255) not null,
    cauhoi text not null,
    cautraloi text not null,
    thoigiancapnhat datetime not null default current_timestamp()
);
select * from dlich;

create table bangtruyvan(
    tenbang text not null, -- tất cả, công nghệ thông tinm...
    tentruyxuat text not null -- chung, CNTT,...
);
insert into bangtruyvan (tenbang, tentruyxuat) values ('tất cả', 'chung');
insert into bangtruyvan (tenbang, tentruyxuat) values ('Công nghệ thông tin', 'CNTT');
select * from bangtruyvan;

create table quanlyadmin(
    id int not null primary key auto_increment,
    hovaten text not null,
    taikhoan varchar(50) not null,
    matkhau	varchar(50) not null
);
select id, hovaten, taikhoan, matkhau from quanlyadmin;
select id, hovaten, taikhoan, matkhau from quanlyadmin where taikhoan = 'khang';
insert into quanlyadmin (hovaten, taikhoan, matkhau) values ('nguyễn mạnh quốc khang', 'khang', 'khang123');
update quanlyadmin set hovaten = '"+matk+"', taikhoan = '"+cauhoi+"', matkhau = '"+cautl+"' where id = "+id+";
SET SQL_SAFE_UPDATES = 0;
update quanlyadmin set matkhau = 'khangnguyen' where taikhoan = 'khang412'