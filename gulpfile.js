'use strict';

var gulp = require('gulp'),
	sass = require('gulp-sass')

gulp.task('sass', function() {
	gulp.src('mainapp/static/mainapp/sass/**/*.scss')
		.pipe(sass())
		.pipe(gulp.dest('mainapp/static/mainapp/css/'))
})	