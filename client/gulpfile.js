var gulp = require('gulp');
var sass = require('gulp-ruby-sass');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var imagemin = require('gulp-imagemin');
var jshint = require('gulp-jshint');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var cache = require('gulp-cache');
var livereload = require('gulp-livereload');
var del = require('del');


gulp.task('styles-dev', function() {
    return gulp.src(['src/vendor/css/**/*.css', 'src/slicknot/css/**/*.css'])
        .pipe(concat('main.css'))
        .pipe(gulp.dest('dist/css'));
});

gulp.task('scripts-dev', function() {
    return gulp.src(['src/vendor/js/angular.js', 'src/vendor/js/modules/**/*.js', 'src/slicknot/js/**/*.js'])
        .pipe(concat('main.js'))
        .pipe(gulp.dest('dist/js'));
});

gulp.task('styles-prod', function() {
    return gulp.src(['src/vendor/css/**/*.css', 'src/slicknot/css/**/*.css'])
        .pipe(concat('main.css'))
        .pipe(minifycss())
        .pipe(gulp.dest('dist/css'));
});

gulp.task('scripts-prod', function() {
    return gulp.src(['src/vendor/js/**/*.js', 'src/slicknot/js/**/*.js'])
        .pipe(concat('main.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist/js'));
});

gulp.task('default', function() {
    gulp.start('styles-dev', 'scripts-dev');
});

gulp.task('prod', function() {
    gulp.start('styles-prod', 'scripts-prod');
});