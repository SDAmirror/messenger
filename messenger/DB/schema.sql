create table authentication_session
(
    session_id          uuid               not null
        constraint authentication_session_pk
            primary key,
    username            varchar(50),
    token               text,
    mac_address         varchar(255),
    os                  text,
    other_info          text,
    authentication_date date default now() not null,
    authentication_time time default now()
);

alter table authentication_session
    owner to postgres;

create unique index authentication_session_session_id_uindex
    on authentication_session (session_id);


create table message
(
    id        uuid,
    content   text,
    send_date date    default now(),
    send_time time    default now(),
    sender    varchar(100),
    receiver  varchar(100),
    sent      boolean default false
);

alter table message
    owner to postgres;




create table message_info
(
    id       uuid not null
        constraint message_info_pk
            primary key,
    sender   varchar(100),
    receiver varchar(100),
    sent     boolean default false
);

alter table message_info
    owner to postgres;

create unique index message_info_id_uindex
    on message_info (id);




create table messages
(
    id              uuid not null
        constraint messages_pk
            primary key,
    message_content text,
    send_date       date default now(),
    send_time       time default now()
);

alter table messages
    owner to postgres;

create unique index messages_id_uindex
    on messages (id);




create table user_base
(
    id       uuid        not null
        constraint user_base_pk
            primary key,
    username varchar(50) not null,
    password varchar(255),
    email    varchar(255)
);

alter table user_base
    owner to postgres;

create unique index user_base_id_uindex
    on user_base (id);

create unique index user_base_username_uindex
    on user_base (username);


insert into public.user_base (id, username, password, email)
values  ('79a07764-43cb-42d4-b64f-2cd114924515', 'user1', 'password1', 'flamehst@mail.ru'),
        ('3dc7a223-49d2-4289-a460-d478f0a77e29', 'user3', 'password3', 'email3'),
        ('40fd327a-e401-45e5-8873-083774c465e8', 'user4', 'password3', 'email3'),
        ('6ed473e1-9c10-4b0a-88e0-74c0ddae492c', 'user6', 'password3', 'email3'),
        ('b3a1580f-0463-4671-89ac-a2bfdbaef2d5', 'user5', 'password3', 'email3'),
        ('5d9c23cb-911a-4a3d-af68-d9c5c1b77bb6', 'user5w', 'password3', 'email3'),
        ('f8ecaf3b-cc3b-4877-9f9c-61c4e9435297', 'useryw', 'password3', 'flamehst@mail.ru'),
        ('ab560603-68bf-4f25-baed-296640ae25ef', 'usery222w', 'password3', 'flamehst@mail.ru'),
        ('ee356511-7fbb-4a5d-a5b1-b340fdea87f0', 'usery2222w', 'password3', 'flamehst@mail.ru'),
        ('168696f1-08cf-4f5e-84d1-1ba09bf998b3', 'usery3333w', 'password3', 'myvideoboxdsa@gmail.com'),
        ('390194bd-0b47-4ad5-a2db-c7f522f824ca', 'userdf3333w', 'password3', 'myvideoboxdsa@gmail.com'),
        ('82ac2bdc-c214-4de8-81ec-c522c3a89180', 'usewdwrdf3333w', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('dba74c4b-9295-4d78-8c02-66b282bfc046', 'usewdwwdawdawrdf3333w', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('e584983b-aeff-4a93-896d-e5a6d36b0c15', 'usewdwwdawdwdwdwrdf3333w', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('c2c1b84d-894f-43b3-b616-573b570f8a0f', 'usewdwwdawdwdwdwdwqdqwrdf3333w', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('c002e369-7522-48a3-a278-b03fefc15dc2', 'usewdawdwdwwdawdwdwdwdwqdqwrdf3333w', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('0aabb5b4-9fe2-48f2-bf2e-debdd4a99001', '5858d', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('48243158-b7a7-4cc2-9de5-2a35c4dd7410', '5828d', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('2219defd-afa5-4897-9d24-d9230b53674e', '582ww8d', 'passwordww3', 'myvideoboxdsa@gmail.com'),
        ('e1b84ee3-809a-4c33-84f2-9038e9dc5e36', '58wq2w1w8d', 'passwordww3', 'myvideoboxdsa@gmail.com');


create table user_profile
(
    profile_id uuid         not null
        constraint user_profile_pk
            primary key,
    user_id    uuid,
    first_name varchar(255) not null,
    last_name  varchar(50),
    is_active  boolean
);

alter table user_profile
    owner to postgres;

create unique index user_profile_profile_id_uindex
    on user_profile (profile_id);


insert into public.user_profile (profile_id, user_id, first_name, last_name, is_active)
values  ('6f189740-2ecc-40b7-a47a-241e1112084f', '79a07764-43cb-42d4-b64f-2cd114924515', 'Damir', 'Sadykov', true),
        ('1d66e7a4-1365-4eb8-a33a-e80f62551700', '3dc7a223-49d2-4289-a460-d478f0a77e29', 'first_name3', 'last_name3', false),
        ('35d3c0cd-ef11-4a71-b1bb-e08fb4f159ba', '40fd327a-e401-45e5-8873-083774c465e8', 'first_name3', 'last_name3', false),
        ('6d331087-a298-451a-a4f6-fd6235c304ec', '6ed473e1-9c10-4b0a-88e0-74c0ddae492c', 'first_name3', 'last_name3', false),
        ('d70ce5d9-e0dc-4b35-be2f-06c5c029d936', 'b3a1580f-0463-4671-89ac-a2bfdbaef2d5', 'first_name3', 'last_name3', false),
        ('fd157639-58b8-4dab-83e2-b8cfb586b485', '5d9c23cb-911a-4a3d-af68-d9c5c1b77bb6', 'first_name3', 'last_name3', false),
        ('41b8fe86-3ebd-4e34-a205-456d33d60c37', 'f8ecaf3b-cc3b-4877-9f9c-61c4e9435297', 'first_name3', 'last_name3', false),
        ('61f17d6f-9ca4-40a6-ac9e-2ea998f90eb0', 'ab560603-68bf-4f25-baed-296640ae25ef', 'first_name3', 'last_name3', false),
        ('30c9d26b-923d-4a49-a05c-29ffe61fa798', 'ee356511-7fbb-4a5d-a5b1-b340fdea87f0', 'first_name3', 'last_name3', false),
        ('28d9db37-5e38-4ab0-b7af-64f55ae15f1a', '168696f1-08cf-4f5e-84d1-1ba09bf998b3', 'first_name3', 'last_name3', false),
        ('588e3243-b6cf-45c8-bd67-3275f67628d1', '390194bd-0b47-4ad5-a2db-c7f522f824ca', 'first_name3', 'last_name3', false),
        ('0212d78b-b11c-4ce7-9d2a-1a838f5aeb32', '82ac2bdc-c214-4de8-81ec-c522c3a89180', 'first_name3', 'last_name3', false),
        ('c38351c7-1162-4cd0-95e8-eecbd735d342', 'dba74c4b-9295-4d78-8c02-66b282bfc046', 'first_name3', 'last_name3', false),
        ('b1df9dbb-07b3-427b-8c1f-134b05d76d91', 'e584983b-aeff-4a93-896d-e5a6d36b0c15', 'first_name3', 'last_name3', false),
        ('1e3164e1-f89c-49b9-b23f-735b9d5aeceb', 'c2c1b84d-894f-43b3-b616-573b570f8a0f', 'first_name3', 'last_name3', false),
        ('bcab579c-1780-4eb0-8686-e9a4a9a38cb2', 'c002e369-7522-48a3-a278-b03fefc15dc2', 'first_name3', 'last_name3', false),
        ('00324177-d1b7-4c2f-acd6-7e05223d26db', '0aabb5b4-9fe2-48f2-bf2e-debdd4a99001', 'first_name3', 'last_name3', false),
        ('313431e4-1b82-47ac-8258-96dc449e8878', '48243158-b7a7-4cc2-9de5-2a35c4dd7410', 'first_name3', 'last_name3', false),
        ('06f2bb06-4a8d-44df-ba86-61368411f60d', '2219defd-afa5-4897-9d24-d9230b53674e', 'first_name3', 'last_name3', false),
        ('1da002b7-3f1f-41e5-8350-47e5e536d90f', 'e1b84ee3-809a-4c33-84f2-9038e9dc5e36', 'first_name3', 'last_name3', false);

