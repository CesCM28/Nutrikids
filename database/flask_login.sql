-- Creación de la table de user

CREATE TABLE user (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  username varchar(20) NOT NULL,
  password char(102) COLLATE utf8_unicode_ci NOT NULL,
  fullname varchar(50) NOT NULL,
  PRIMARY KEY (id)
);

-- Creación de la table de colonia,
-- esta relacionada con Municipio

CREATE TABLE colonia (
    id int NOT NULL AUTO_INCREMENT,
    idMunicipio int,
    name varchar(100) NOT NULL,
    cp varchar(5),
    state tinyint(1) default 1,
    PRIMARY KEY (id)
); 

-- Creación de la table de escuela
-- esta realcionada con Colonia

CREATE TABLE escuela (
    id int NOT NULL AUTO_INCREMENT,
    idColonia int,
    cp varchar(5),
    name varchar(100) NOT NULL,
    street varchar(200) NOT NULL,
    number varchar(10) NOT NULL,
    state tinyint(1) default 1,
    PRIMARY KEY (id)
);

-- Creación de la tabla puesto
CREATE TABLE puesto (
    id smallint NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    state tinyint(1) default 1,
    PRIMARY KEY (id)
);

-- Insert de la tabla puesto
INSERT INTO puesto (name) VALUES ("Director");
INSERT INTO puesto (name) VALUES ("Profesor");

-- Creación de la tabla puesto
CREATE TABLE genero (
    id smallint NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    state tinyint(1) default 1,
    PRIMARY KEY (id)
);

-- Insert de la tabla puesto
INSERT INTO genero (name) VALUES ("Femenino");
INSERT INTO genero (name) VALUES ("Masculino");

-- Creación de la table de docente
-- esta realcionada con escuela, puesto y genero

CREATE TABLE docente (
    id int NOT NULL AUTO_INCREMENT,
    idEscuela int, --
    idPosition smallint, --
    idGender smallint, --
    names varchar(100),
    lastName varchar(50),
    secondLastName varchar(50),
    edad number,
    state tinyint(1) default 1,
    PRIMARY KEY (id)
);

-- Volcado de datos para la tabla user

INSERT INTO user (id, username, password, fullname) VALUES
(1, 'CCARDENAS', 'pbkdf2:sha256:260000$fiRyeVmApEki8uvm$40d93cdea3f941010f3eedfafd228db15c41810ce625a691ff8cb2491300b010', 'Cesar Cardenas');