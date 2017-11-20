CREATE DATABASE alfredsDb;
CREATE TABLE `alfredsDb`.`new_table` (
  `id` INT NOT NULL,
  `description` TEXT NULL,
  `tag` VARCHAR(45) NULL,
  `priority` VARCHAR(45) NULL,
  `day_of_week` VARCHAR(45) NULL,
  `hour` TIME NULL,
  PRIMARY KEY (`id`));
ALTER TABLE `alfredsDb`.`new_table` RENAME TO  `alfredsDb`.`user_activities` ;
ALTER TABLE `alfredsDb`.`user_activities`
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ;
INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour)
    VALUES ('Trabalho CES-122', 'ITA', 'Média', 'MON', '14:59');
INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour)
    VALUES ('Prova GEO', 'Curso', 'Baixa', 'FRI', '08:00');
INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour)
    VALUES ('Ir passear com o cachorro', 'Pessoal', 'Baixa', 'SAT', '17:00');
INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour)
    VALUES ('Ir no cinema', 'Pessoal', 'Alta', 'SUN', '20:00');
INSERT INTO alfredsDb.user_activities (description, tag, priority, day_of_week, hour)
    VALUES ('Cabelereiro', 'Pessoal', 'Média', 'WED', '16:00');
