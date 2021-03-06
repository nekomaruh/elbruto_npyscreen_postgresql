PGDMP     7    1                x            elbruto    10.13    10.13                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    25930    elbruto    DATABASE     �   CREATE DATABASE elbruto WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Chile.1252' LC_CTYPE = 'Spanish_Chile.1252';
    DROP DATABASE elbruto;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false                       0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    25939    administrador    TABLE     >   CREATE TABLE public.administrador (
    nick text NOT NULL
);
 !   DROP TABLE public.administrador;
       public         postgres    false    3            �            1259    25965    avatar    TABLE     �   CREATE TABLE public.avatar (
    nick text NOT NULL,
    nivel integer NOT NULL,
    ptosexp integer NOT NULL,
    ptosvelocidad integer NOT NULL,
    ptosvida integer NOT NULL,
    ptosataque integer NOT NULL
);
    DROP TABLE public.avatar;
       public         postgres    false    3            �            1259    25952    jugador    TABLE     {   CREATE TABLE public.jugador (
    nick text NOT NULL,
    baneadosn boolean NOT NULL,
    cantreportes integer NOT NULL
);
    DROP TABLE public.jugador;
       public         postgres    false    3            �            1259    25978    reporta    TABLE     Y   CREATE TABLE public.reporta (
    nick text NOT NULL,
    nickreportado text NOT NULL
);
    DROP TABLE public.reporta;
       public         postgres    false    3            �            1259    25931    usuario    TABLE     �   CREATE TABLE public.usuario (
    nick text NOT NULL,
    contrasena text NOT NULL,
    nombre text NOT NULL,
    email text NOT NULL,
    pais text NOT NULL
);
    DROP TABLE public.usuario;
       public         postgres    false    3            
          0    25939    administrador 
   TABLE DATA               -   COPY public.administrador (nick) FROM stdin;
    public       postgres    false    197   �                 0    25965    avatar 
   TABLE DATA               [   COPY public.avatar (nick, nivel, ptosexp, ptosvelocidad, ptosvida, ptosataque) FROM stdin;
    public       postgres    false    199                    0    25952    jugador 
   TABLE DATA               @   COPY public.jugador (nick, baneadosn, cantreportes) FROM stdin;
    public       postgres    false    198   e                 0    25978    reporta 
   TABLE DATA               6   COPY public.reporta (nick, nickreportado) FROM stdin;
    public       postgres    false    200   �       	          0    25931    usuario 
   TABLE DATA               H   COPY public.usuario (nick, contrasena, nombre, email, pais) FROM stdin;
    public       postgres    false    196   �       �
           2606    25946     administrador administrador_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (nick);
 J   ALTER TABLE ONLY public.administrador DROP CONSTRAINT administrador_pkey;
       public         postgres    false    197            �
           2606    25972    avatar avatar_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.avatar
    ADD CONSTRAINT avatar_pkey PRIMARY KEY (nick);
 <   ALTER TABLE ONLY public.avatar DROP CONSTRAINT avatar_pkey;
       public         postgres    false    199            �
           2606    25959    jugador jugador_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_pkey PRIMARY KEY (nick);
 >   ALTER TABLE ONLY public.jugador DROP CONSTRAINT jugador_pkey;
       public         postgres    false    198            �
           2606    25985    reporta reporta_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.reporta
    ADD CONSTRAINT reporta_pkey PRIMARY KEY (nick, nickreportado);
 >   ALTER TABLE ONLY public.reporta DROP CONSTRAINT reporta_pkey;
       public         postgres    false    200    200            �
           2606    25938    usuario usuario_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (nick);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public         postgres    false    196            �
           2606    25947 %   administrador administrador_nick_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_nick_fkey FOREIGN KEY (nick) REFERENCES public.usuario(nick);
 O   ALTER TABLE ONLY public.administrador DROP CONSTRAINT administrador_nick_fkey;
       public       postgres    false    196    2690    197            �
           2606    25973    avatar avatar_nick_fkey    FK CONSTRAINT     w   ALTER TABLE ONLY public.avatar
    ADD CONSTRAINT avatar_nick_fkey FOREIGN KEY (nick) REFERENCES public.jugador(nick);
 A   ALTER TABLE ONLY public.avatar DROP CONSTRAINT avatar_nick_fkey;
       public       postgres    false    2694    198    199            �
           2606    25960    jugador jugador_nick_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.jugador
    ADD CONSTRAINT jugador_nick_fkey FOREIGN KEY (nick) REFERENCES public.usuario(nick);
 C   ALTER TABLE ONLY public.jugador DROP CONSTRAINT jugador_nick_fkey;
       public       postgres    false    2690    196    198            �
           2606    25986    reporta reporta_nick_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.reporta
    ADD CONSTRAINT reporta_nick_fkey FOREIGN KEY (nick) REFERENCES public.jugador(nick);
 C   ALTER TABLE ONLY public.reporta DROP CONSTRAINT reporta_nick_fkey;
       public       postgres    false    200    198    2694            �
           2606    25991 "   reporta reporta_nickreportado_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reporta
    ADD CONSTRAINT reporta_nickreportado_fkey FOREIGN KEY (nickreportado) REFERENCES public.jugador(nick);
 L   ALTER TABLE ONLY public.reporta DROP CONSTRAINT reporta_nickreportado_fkey;
       public       postgres    false    2694    198    200            
      x�KL�������� 9�         F   x����3�4�4�4�4"���(b1��K���4�42�4�44��ʮ̯*7�0�4����� :�         ,   x����3�L�4���H�14�0+�c����| Ð+F��� ��
m         +   x��K���̮̯��y@.WvFb��D47?����� �>      	   �   x�5�M
�@�u�s���REq�&��64&2?�=�������)��z�����I��9/�#��(B}aK�Eꁅ����+��
u��}�I3+��i���)�w����&�pV�R�a&8͕;e������vOV ic��iʨ�S���v%�*�>Vι/^TJ	     