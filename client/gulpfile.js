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


gulp.task('styles', function() {
    return gulp.src(['src/vendor/css/**/*.css', 'src/slicknot/css/**/*.css'])
        .pipe(concat('main.css'))
        .pipe(minifycss())
        .pipe(gulp.dest('dist/assets/css'));
});

gulp.task('scripts', function() {
    return gulp.src(['src/vendor/js/**/*.js', 'src/slicknot/js/**/*.js'])
        .pipe(concat('main.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist/assets/js'));
});

gulp.task('default', function() {
    gulp.start('styles', 'scripts');
});