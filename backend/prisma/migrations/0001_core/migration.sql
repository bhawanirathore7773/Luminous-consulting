CREATE TABLE `services` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  `slug` VARCHAR(140) NOT NULL,
  `short_summary` VARCHAR(200) NOT NULL,
  `hero_intro` TEXT NOT NULL,
  `business_problem` TEXT NOT NULL,
  `delivery_approach` TEXT NOT NULL,
  `engagement_model` TEXT NOT NULL,
  `who_its_for` TEXT NOT NULL,
  `cta_label` VARCHAR(80) NOT NULL,
  `meta_title` VARCHAR(70) NULL,
  `meta_description` VARCHAR(160) NULL,
  `featured` BOOLEAN NOT NULL DEFAULT false,
  `sort_order` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated_at` DATETIME(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `services_slug_key` (`slug`),
  INDEX `services_featured_sort_order_idx` (`featured`, `sort_order`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `industries` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  `slug` VARCHAR(140) NOT NULL,
  `short_summary` VARCHAR(200) NOT NULL,
  `hero_intro` TEXT NOT NULL,
  `sap_landscape` TEXT NOT NULL,
  `outcomes` TEXT NOT NULL,
  `cta_label` VARCHAR(80) NOT NULL,
  `meta_title` VARCHAR(70) NULL,
  `meta_description` VARCHAR(160) NULL,
  `sort_order` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated_at` DATETIME(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `industries_slug_key` (`slug`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE `solutions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(120) NOT NULL,
  `slug` VARCHAR(140) NOT NULL,
  `short_summary` VARCHAR(200) NOT NULL,
  `hero_intro` TEXT NOT NULL,
  `business_problem` TEXT NOT NULL,
  `approach` TEXT NOT NULL,
  `who_its_for` TEXT NOT NULL,
  `cta_label` VARCHAR(80) NOT NULL,
  `meta_title` VARCHAR(70) NULL,
  `meta_description` VARCHAR(160) NULL,
  `sort_order` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `updated_at` DATETIME(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `solutions_slug_key` (`slug`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;