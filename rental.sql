/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     21/11/2019 21:05:32                          */
/*==============================================================*/


drop table if exists KENDARAAN;

drop table if exists PEGAWAI;

drop table if exists PEMINJAM;

drop table if exists RENTAL;

/*==============================================================*/
/* Table: KENDARAAN                                             */
/*==============================================================*/
create table KENDARAAN
(
   ID_KENDARAAN         int not null,
   NAMA_KENDARAAN       varchar(1024),
   MERK_KENDARAAN       varchar(1024),
   JENIS_KENDARAAN      varchar(1024),
   JUMLAH_KENDARAAN     int,
   primary key (ID_KENDARAAN)
);

/*==============================================================*/
/* Table: PEGAWAI                                               */
/*==============================================================*/
create table PEGAWAI
(
   ID_PEGAWAI           int not null,
   NAMA_PEGAWAI         varchar(1024),
   USERNAME             varchar(1024),
   PASSWORD             varchar(1024),
   primary key (ID_PEGAWAI)
);

/*==============================================================*/
/* Table: PEMINJAM                                              */
/*==============================================================*/
create table PEMINJAM
(
   NIK                  bigint not null,
   NAMA_PEMINJAM        varchar(1024),
   ALAMAT_PEMINJAM      varchar(1024),
   TGL_DAFTAR           datetime,
   primary key (NIK)
);

/*==============================================================*/
/* Table: RENTAL                                                */
/*==============================================================*/
create table RENTAL
(
   ID_RENTAL            int not null AUTO_INCREMENT,
   ID_PEGAWAI           int,
   ID_KENDARAAN         int,
   NIK                  bigint,
   TANGGAL_RENTAL       datetime,
   STATUS_RENTAL        varchar(1024),
   primary key (ID_RENTAL)
);

alter table RENTAL add constraint FK_RELATIONSHIP_2 foreign key (ID_PEGAWAI)
      references PEGAWAI (ID_PEGAWAI) on delete restrict on update restrict;

alter table RENTAL add constraint FK_RELATIONSHIP_3 foreign key (ID_KENDARAAN)
      references KENDARAAN (ID_KENDARAAN) on delete restrict on update restrict;

alter table RENTAL add constraint FK_RELATIONSHIP_4 foreign key (NIK)
      references PEMINJAM (NIK) on delete restrict on update restrict;

