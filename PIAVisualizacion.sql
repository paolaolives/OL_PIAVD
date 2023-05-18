-- Crear tabla usuario
create table usuario (
  id_usuario int primary key auto_increment,
  nombre_usuario varchar(50),
  correo varchar(50),
  contrasena varchar(50)
);

-- Crear tabla reseña
create table resena (
  id_resena int primary key auto_increment,
  id_usuario int,
  titulo varchar(100),
  genero varchar(50),
  calificacion tinyint,
  texto text,
  foreign key (id_usuario) references usuario(id_usuario)
);

-- Datos
insert into usuario (nombre_usuario, correo, contrasena)
values 
('Headbot', 'headbot@gmail.com', 'contrasena'),
('DevAsh', 'devash@hotmail.com', 'contrasena'),
('PakYuna', 'pakyuna@outlook.com', 'contrasena');

insert into resena (id_usuario, titulo, genero, calificacion, texto) 
values 
(1, 'Parásitos', 'Drama', 10,'Esta es una gran película, definitivamente una de las mejores de ese año.'),
(2, 'El castillo vagabundo', 'Animación',10,'Una de mis favoritas!');

select u.id_usuario, u.nombre_usuario,r.id_resena, r.titulo, r.genero, r.calificacion, r.texto from usuario u 
join resena r on r.id_usuario = u.id_usuario;