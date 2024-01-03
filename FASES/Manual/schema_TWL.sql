-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema the_wine_lab
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema the_wine_lab
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `the_wine_lab` DEFAULT CHARACTER SET utf8 ;
USE `the_wine_lab` ;

-- -----------------------------------------------------
-- Table `the_wine_lab`.`1_wine_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `the_wine_lab`.`1_wine_info` (
  `name_w` VARCHAR(200) NOT NULL,
  `year_w` VARCHAR(10) NOT NULL,
  `region` VARCHAR(50) NULL,
  PRIMARY KEY (`name_w`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `the_wine_lab`.`2_scoring`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `the_wine_lab`.`2_scoring` (
  `number_score` INT NOT NULL AUTO_INCREMENT,
  `user_score` DECIMAL(4,2) NULL,
  `pk_score` DECIMAL(4,2) NULL,
  `pn_score` DECIMAL(4,2) NULL,
  `sk_score` DECIMAL(4,2) NULL,
  `1_wine_info_name_w` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`number_score`),
  INDEX `fk_2_scoring_1_wine_info_idx` (`1_wine_info_name_w` ASC) VISIBLE,
  CONSTRAINT `fk_2_scoring_1_wine_info`
    FOREIGN KEY (`1_wine_info_name_w`)
    REFERENCES `the_wine_lab`.`1_wine_info` (`name_w`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `the_wine_lab`.`3_wine_type_price`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `the_wine_lab`.`3_wine_type_price` (
  `wine_order` INT NOT NULL AUTO_INCREMENT,
  `price` DECIMAL(5,3) NULL,
  `alcohol_content` DECIMAL(5,3) NULL,
  `wine_grape` VARCHAR(200) NULL,
  `type_w` VARCHAR(200) NULL,
  `1_wine_info_name_w` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`wine_order`),
  INDEX `fk_3_wine_type_price_1_wine_info1_idx` (`1_wine_info_name_w` ASC) VISIBLE,
  CONSTRAINT `fk_3_wine_type_price_1_wine_info1`
    FOREIGN KEY (`1_wine_info_name_w`)
    REFERENCES `the_wine_lab`.`1_wine_info` (`name_w`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
