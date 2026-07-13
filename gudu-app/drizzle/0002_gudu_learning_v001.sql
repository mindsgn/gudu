CREATE TABLE `app_state` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `course_modules` (
	`id` text PRIMARY KEY NOT NULL,
	`course_id` text NOT NULL,
	`slug` text NOT NULL,
	`title` text NOT NULL,
	`summary` text,
	`sort_order` integer NOT NULL,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL,
	FOREIGN KEY (`course_id`) REFERENCES `courses`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `course_modules_course_idx` ON `course_modules` (`course_id`,`sort_order`);--> statement-breakpoint
CREATE TABLE `courses` (
	`id` text PRIMARY KEY NOT NULL,
	`slug` text NOT NULL,
	`title` text NOT NULL,
	`description` text NOT NULL,
	`source_index_path` text NOT NULL,
	`total_lessons` integer NOT NULL,
	`total_modules` integer NOT NULL,
	`sort_order` integer NOT NULL,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE INDEX `courses_slug_idx` ON `courses` (`slug`);--> statement-breakpoint
CREATE TABLE `daily_activity` (
	`activity_date` text PRIMARY KEY NOT NULL,
	`points_earned` integer NOT NULL,
	`lessons_completed` integer NOT NULL,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `learner_profile` (
	`id` text PRIMARY KEY NOT NULL,
	`total_points` integer NOT NULL,
	`current_streak` integer NOT NULL,
	`longest_streak` integer NOT NULL,
	`last_active_on` text,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `lesson_progress` (
	`lesson_id` text PRIMARY KEY NOT NULL,
	`status` text NOT NULL,
	`scroll_percent` integer NOT NULL,
	`last_scroll_offset` integer NOT NULL,
	`started_at` integer,
	`completed_at` integer,
	`last_opened_at` integer,
	`points_awarded` integer NOT NULL,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL,
	FOREIGN KEY (`lesson_id`) REFERENCES `lessons`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `lesson_progress_status_idx` ON `lesson_progress` (`status`);--> statement-breakpoint
CREATE TABLE `lessons` (
	`id` text PRIMARY KEY NOT NULL,
	`course_id` text NOT NULL,
	`module_id` text NOT NULL,
	`slug` text NOT NULL,
	`title` text NOT NULL,
	`source_path` text NOT NULL,
	`order_index` integer NOT NULL,
	`estimated_study_minutes` integer,
	`estimated_practice_minutes` integer,
	`difficulty_label` text,
	`prerequisites_json` text NOT NULL,
	`unlocked_concepts_json` text NOT NULL,
	`markdown` text NOT NULL,
	`created_at` integer NOT NULL,
	`updated_at` integer NOT NULL,
	FOREIGN KEY (`course_id`) REFERENCES `courses`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`module_id`) REFERENCES `course_modules`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `lessons_course_idx` ON `lessons` (`course_id`,`order_index`);--> statement-breakpoint
CREATE INDEX `lessons_module_idx` ON `lessons` (`module_id`,`order_index`);