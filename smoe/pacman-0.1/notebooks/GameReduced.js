//////////////////////////////////////////////////////
// Group members: Zi Wang (ziw), Bingying Xia(bxia) //
//////////////////////////////////////////////////////
define(function(require, exports, module) {


var canvasID = "myCanvas";
var CANVAS_WIDTH = 0;
var CANVAS_HEIGHT = 0;
var canvas = document.getElementById(canvasID);
var ctx = canvas.getContext("2d");

// game grid
var GRID_WIDTH = 30;
var GRID_HEIGHT = 30;
var WALL_WIDTH = 3;
var numRows = CANVAS_WIDTH/GRID_HEIGHT;
var numCols = CANVAS_HEIGHT/GRID_WIDTH;

// colors for UI & Pacman
var BG_COLOR = "black";
var BORDER_COLOR = "blue";
var BEAN_COLOR = "white";
var PACMAN_COLOR = "yellow";

// colors for ghost
var RED = "red";
var PINK = "#ff9cce";
var CYAN = "#00ffde";
var ORANGE = "#ffb847";
var WEAK_COLOR = "#0031ff";
var BLINKING_COLOR = "white";

// size of sprites
var NORMAL_BEAN_RADIUS = 2;
var POWER_BEAN_RADIUS = 5;
var PACMAN_RADIUS = 9;
var GHOST_RADIUS = 9;

// directions
var UP = 1;
var DOWN = 2;
var LEFT = 3;
var RIGHT = 4;

// game parameters
var intervalId;
var restartTimer = 0;
var timerDelay = 80;
var speed = 5;
var score = 0;
var lives = [];
var MAX_LIFE = 3;
var life = MAX_LIFE;
var weakBonus = 200;
var MAX_BEANS = 136;
var beansLeft = MAX_BEANS;
var weakCounter;
var WEAK_DURATION = 10000/timerDelay;


//bean cases
var NORMAL_BEAN = 1
var POWER_BEAN = 2;

//spirtes instances
var welcomePacman;
var welcomeBlinky;
var welcomeInky;
var mrPacman;
var ghosts = [];

//game state and map
var gameOn = false;
var gamePaused = false;
var maze;

//********************************************************************************
var id = -1;

//wall cases

var GridConstants = {
    CROSS_RD: 0, //no wall
    LEFT_ONLY: 1,
    TOP_ONLY: 2,
    RIGHT_ONLY: 4,
    BOTTOM_ONLY: 8,
    LEFT_RIGHT: 5,
    LEFT_TOP: 3,
    LEFT_BOTTOM: 9,
    RIGHT_TOP: 6,
    RIGHT_BOTTOM: 12,
    TOP_BOTTOM: 10,
    BOTTOM_LEFT_TOP: 11,
    LEFT_TOP_RIGHT: 7,
    TOP_RIGHT_BOTTOM: 14,
    RIGHT_BOTTOM_LEFT: 13,
    EMPTY_GRID: 0,
    CLOSED_GRID: 15
}


function Grid (xCord, yCord, gridType, beanType) {
    this.x = xCord;
    this.y = yCord;
    this.gridType = gridType===undefined? GridConstants.EMPTY_GRID : gridType;
    this.beanType = beanType;
}

Grid.prototype.getRow = function() {
    return getRowIndex(this.y);
};

Grid.prototype.getCol = function() {
    return getColIndex(this.x);
};

Grid.prototype.hasBean = true;


Grid.prototype.toString = function() {
    return "Grid ("+this.x+","+this.y+") - Grid Type: " + this.gridType;
};

Grid.prototype.draw = function() {
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(this.x, this.y, GRID_WIDTH, GRID_HEIGHT);
    var gridType = this.gridType    ;
    if(gridType === undefined || gridType === GridConstants.EMPTY_GRID){
        this.drawBean();
        return;
    }
    switch(gridType){

        case GridConstants.LEFT_ONLY:
        this.addLeftEdge();
        break;

        case GridConstants.RIGHT_ONLY:
        this.addRightEdge();
        break;

        case GridConstants.TOP_ONLY:
        this.addTopEdge();
        break;

        case GridConstants.BOTTOM_ONLY:
        this.addBottomEdge();
        break;

        case GridConstants.LEFT_RIGHT:
        this.addLeftEdge();
        this.addRightEdge();
        break;

        case GridConstants.LEFT_TOP:
        this.addLeftEdge();
        this.addTopEdge();
        break;

        case GridConstants.LEFT_BOTTOM:
        this.addLeftEdge();
        this.addBottomEdge();
        break;

        case GridConstants.RIGHT_TOP:
        this.addRightEdge();
        this.addTopEdge();
        break;

        case GridConstants.RIGHT_BOTTOM:
        this.addRightEdge();
        this.addBottomEdge();
        break;

        case GridConstants.TOP_BOTTOM:
        this.addTopEdge();
        this.addBottomEdge();
        break;

        case GridConstants.CROSS_RD:
        this.makeCrossRoad();
        break;

        case GridConstants.LEFT_TOP_RIGHT:
        this.addLeftEdge();
        this.addTopEdge();
        this.addRightEdge();
        break;

        case GridConstants.TOP_RIGHT_BOTTOM:
        this.addTopEdge();
        this.addRightEdge();
        this.addBottomEdge();
        break;

        case GridConstants.RIGHT_BOTTOM_LEFT:
        this.addRightEdge();
        this.addBottomEdge();
        this.addLeftEdge();
        break;

        case GridConstants.BOTTOM_LEFT_TOP:
        this.addBottomEdge();
        this.addLeftEdge();
        this.addTopEdge();
        break;

        case GridConstants.CLOSED_GRID:
        this.addLeftEdge();
        this.addTopEdge();
        this.addBottomEdge();
        this.addRightEdge();
        break;

        default:
        break;
    }
    this.drawBean();    
};

Grid.prototype.addLeftEdge = function() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(this.x, this.y, WALL_WIDTH, GRID_HEIGHT);
};

Grid.prototype.addRightEdge = function() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(this.x+GRID_WIDTH - WALL_WIDTH , this.y, WALL_WIDTH , GRID_HEIGHT);
};

Grid.prototype.addTopEdge = function() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(this.x, this.y, GRID_WIDTH, WALL_WIDTH);
};

Grid.prototype.addBottomEdge = function() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(this.x, this.y + GRID_HEIGHT - WALL_WIDTH, GRID_WIDTH, WALL_WIDTH);
};

Grid.prototype.makeCrossRoad = function() {
    ctx.fillStyle = BORDER_COLOR;
    ctx.fillRect(this.x, this.y, WALL_WIDTH, WALL_WIDTH);
    ctx.fillRect(this.x + GRID_WIDTH - WALL_WIDTH, this.y, WALL_WIDTH, WALL_WIDTH);
    ctx.fillRect(this.x, this.y + GRID_HEIGHT - WALL_WIDTH, WALL_WIDTH, WALL_WIDTH);
    ctx.fillRect(this.x + GRID_WIDTH - WALL_WIDTH, this.y + GRID_HEIGHT - WALL_WIDTH, WALL_WIDTH, WALL_WIDTH);

};

//draw a bean at the center of this grid
Grid.prototype.drawBean = function() {
    var beanType = this.beanType;
    var centerX = this.x + GRID_WIDTH/2;
    var centerY = this.y + GRID_HEIGHT/2;

    ctx.fillStyle = BEAN_COLOR;
    if(beanType === undefined){
        return;
    }

    if(beanType === NORMAL_BEAN){
        circle(ctx, centerX, centerY, NORMAL_BEAN_RADIUS);
    }
    else if(beanType === POWER_BEAN){
        circle(ctx, centerX, centerY, POWER_BEAN_RADIUS);
    }
    else{
        //unkwon bean type
        return;
    }
};

var gc = GridConstants;

var mazeContent = []
// grids that don't redraw
var staticGrids = [];
var staticGridsIndex = 0;

var beanPositions = []

var powerBeanPositions = [];

// ghost house
var ghostHouse = [];
var ghostHouseIndex = 0;

/*======================END GLOBAL VARs====================*/

/*======================Start pacman====================*/

function Pacman(xCord, yCord, direction){
    this.x = xCord;
    this.y = yCord;
    this.dir = direction;
    this.nextDir = undefined; //the direction to turn at next available turning point
    this.radius = PACMAN_RADIUS;
    this.mouthOpen = true;
}


Pacman.prototype.draw = function(color) {
    if (color == undefined){
        ctx.fillStyle = PACMAN_COLOR;
    }
    else{
        ctx.fillStyle = color;
    }
    ctx.beginPath();

    if (!this.mouthOpen){
        switch(this.dir){
            case UP:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*11/18, 2*Math.PI-Math.PI*7/18, true);
            break;

            case DOWN:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*29/18, 2*Math.PI-Math.PI*25/18, true);
            break;

            case LEFT:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*10/9, 2*Math.PI-Math.PI*8/9, true);
            break;

            case RIGHT:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI/9, 2*Math.PI-Math.PI*17/9, true);
            break;

            default:
            break;
        }
    }
    else {
        switch(this.dir){
            case UP:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*7/9, 2*Math.PI-Math.PI*2/9, true);
            break;

            case DOWN:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*16/9, 2*Math.PI-Math.PI*11/9, true);
            break;

            case LEFT:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*23/18, 2*Math.PI-Math.PI*13/18, true);
            break;

            case RIGHT:
            ctx.arc(this.x, this.y, this.radius, 2*Math.PI-Math.PI*5/18, 2*Math.PI-Math.PI*31/18, true);
            break;

            default:
            break;
        }
    }
    ctx.lineTo(this.x, this.y);
    ctx.fill();
};

//get the row index of current location
Pacman.prototype.getRow = function() {
    return getRowIndex(this.y);
};

//get the col index of current location
Pacman.prototype.getCol = function() {
    return getColIndex(this.x);
};

//return if pacman can move with current direction & tile
Pacman.prototype.canMove = function(dir) {
    return canMove(this.x, this.y, dir);
};

//try to turn(if necessary) and move the pacman.
Pacman.prototype.move = function() {
    if(onGridCenter(this.x, this.y) === false){
        //not on a grid center
        if(this.nextDir != undefined &&  (
            (this.dir === UP && this.nextDir === DOWN )||
            (this.dir === DOWN && this.nextDir === UP) ||
            (this.dir === LEFT && this.nextDir === RIGHT) ||
            (this.dir === RIGHT && this.nextDir ===LEFT)
            ))
        {
            this.dir = this.nextDir;
            this.nextDir = undefined;
        }

        this.moveOneStep();

        return;
    }
    else{
        //on grid center. change direction if needed

        if(this.nextDir != undefined && this.canMove(this.nextDir)){
            this.dir = this.nextDir;
            this.nextDir = undefined;
            this.moveOneStep();
        }
        else{
            //check if pacman can keep moving
            if(this.canMove(this.dir)){
                this.moveOneStep();
            }
        }   
    }
};

//move one step in the current direction if allowed
Pacman.prototype.moveOneStep = function() {
    var newX =0;
    var newY =0;
    if(!canMove(this.x, this.y, this.dir)){
        return;
    }
    switch(this.dir){
        case UP:
        newY = this.y  - speed;
        if(newY - this.radius - WALL_WIDTH > 0){
            this.y = newY;
            this.mouthOpen = ! this.mouthOpen;
        }
        break;

        case DOWN:
        newY = this.y + speed;
        if(newY + this.radius + WALL_WIDTH < CANVAS_HEIGHT) {
            this.y = newY;
            this.mouthOpen = ! this.mouthOpen;

        }
        break;


        case LEFT:
        newX = this.x - speed;
        if(newX - this.radius - WALL_WIDTH > 0 ){
            this.x = newX;
            this.mouthOpen = ! this.mouthOpen;
        }
        break;

        case RIGHT:
        newX = this.x + speed;

        if(newX + this.radius + WALL_WIDTH < CANVAS_WIDTH){
            this.x = newX;
            this.mouthOpen = ! this.mouthOpen;
        }
        break;
        
        default:
        break;
    }
};
/*======================END pacman====================*/

/*======================Start ghost====================*/

function Ghost(xCord, yCord, gColor, direction){
    this.x = xCord;
    this.y = yCord;
    this.color = gColor;
    this.dir = direction;
    this.isWeak = false;
    this.radius = GHOST_RADIUS;
    this.isMoving = false;
    this.isBlinking = false;
    this.isDead = false;
    this.speed = speed;
    this.stepCounter = 0;

}


Ghost.prototype.draw = function() {

    if(!this.isDead){
        // body color
        if(this.isWeak){
            if(this.isBlinking){
                ctx.fillStyle = BLINKING_COLOR;
            }
            else{
                ctx.fillStyle = WEAK_COLOR;
            }
        }
        else{
            ctx.fillStyle = this.color;
        }
        
        ctx.beginPath();

        ctx.arc(this.x, this.y, this.radius, Math.PI, 0, false);
        ctx.moveTo(this.x-this.radius, this.y);
        

        // LEGS
        if (!this.isMoving){
            ctx.lineTo(this.x-this.radius, this.y+this.radius);
            ctx.lineTo(this.x-this.radius+this.radius/3, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x-this.radius+this.radius/3*2, this.y+this.radius);
            ctx.lineTo(this.x, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x+this.radius/3, this.y+this.radius);
            ctx.lineTo(this.x+this.radius/3*2, this.y+this.radius-this.radius/4);

            ctx.lineTo(this.x+this.radius, this.y+this.radius);
            ctx.lineTo(this.x+this.radius, this.y);
        }
        else {
            ctx.lineTo(this.x-this.radius, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x-this.radius+this.radius/3, this.y+this.radius);
            ctx.lineTo(this.x-this.radius+this.radius/3*2, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x, this.y+this.radius);
            ctx.lineTo(this.x+this.radius/3, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x+this.radius/3*2, this.y+this.radius);
            ctx.lineTo(this.x+this.radius, this.y+this.radius-this.radius/4);
            ctx.lineTo(this.x+this.radius, this.y);
        }
        
        ctx.fill();
    }


    if(this.isWeak){

        if(this.isBlinking){
            ctx.fillStyle = "#f00";
            ctx.strokeStyle = "f00";
        }
        else{
            ctx.fillStyle = "white";
            ctx.strokeStyle = "white";
        }

        //eyes
        ctx.beginPath();//left eye
        ctx.arc(this.x-this.radius/2.5, this.y-this.radius/5, this.radius/5, 0, Math.PI*2, true); // white
        ctx.fill();

        ctx.beginPath(); // right eye
        ctx.arc(this.x+this.radius/2.5, this.y-this.radius/5, this.radius/5, 0, Math.PI*2, true); // white
        ctx.fill();

        //mouth
        ctx.beginPath();
        ctx.lineWidth=1;
        ctx.moveTo(this.x-this.radius+this.radius/5, this.y+this.radius/2);
        ctx.lineTo(this.x-this.radius+this.radius/3, this.y+this.radius/4);
        ctx.lineTo(this.x-this.radius+this.radius/3*2, this.y+this.radius/2);
        ctx.lineTo(this.x, this.y+this.radius/4);
        ctx.lineTo(this.x+this.radius/3, this.y+this.radius/2);
        ctx.lineTo(this.x+this.radius/3*2, this.y+this.radius/4);
        ctx.lineTo(this.x+this.radius-this.radius/5, this.y+this.radius/2);
        ctx.stroke();
    }
    else{
        // EYES
        ctx.fillStyle = "white"; //left eye
        ctx.beginPath();
        ctx.arc(this.x-this.radius/2.5, this.y-this.radius/5, this.radius/3, 0, Math.PI*2, true); // white
        ctx.fill();

        ctx.fillStyle = "white"; //right eye
        ctx.beginPath();
        ctx.arc(this.x+this.radius/2.5, this.y-this.radius/5, this.radius/3, 0, Math.PI*2, true); // white
        ctx.fill();


        switch(this.dir){

            case UP:
                ctx.fillStyle="black"; //left eyeball
                ctx.beginPath();
                ctx.arc(this.x-this.radius/3, this.y-this.radius/5-this.radius/6, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();

                ctx.fillStyle="black"; //right eyeball
                ctx.beginPath();
                ctx.arc(this.x+this.radius/3, this.y-this.radius/5-this.radius/6, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();
            break;

            case DOWN:
                ctx.fillStyle="black"; //left eyeball
                ctx.beginPath();
                ctx.arc(this.x-this.radius/3, this.y-this.radius/5+this.radius/6, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();

                ctx.fillStyle="black"; //right eyeball
                ctx.beginPath();
                ctx.arc(this.x+this.radius/3, this.y-this.radius/5+this.radius/6, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();
            break;

            case LEFT:
                ctx.fillStyle="black"; //left eyeball
                ctx.beginPath();
                ctx.arc(this.x-this.radius/3-this.radius/5, this.y-this.radius/5, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();

                ctx.fillStyle="black"; //right eyeball
                ctx.beginPath();
                ctx.arc(this.x+this.radius/3-this.radius/15, this.y-this.radius/5, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();
            break;

            case RIGHT:
                ctx.fillStyle="black"; //left eyeball
                ctx.beginPath();
                ctx.arc(this.x-this.radius/3+this.radius/15, this.y-this.radius/5, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();

                ctx.fillStyle="black"; //right eyeball
                ctx.beginPath();
                ctx.arc(this.x+this.radius/3+this.radius/5, this.y-this.radius/5, this.radius/6, 0, Math.PI*2, true); //black
                ctx.fill();
            break;

        }
    }
};

Ghost.prototype.getRow = function() {
    return getRowIndex(this.y);
};

Ghost.prototype.getCol = function() {
    return getColIndex(this.x);
};

//move one step in the current direction if allowed
Ghost.prototype.moveOneStep = function() {
    // body...
    var newX =0;
    var newY =0;
    if(!canMove(this.x, this.y, this.dir)){
        return;
    }
    switch(this.dir){

        case UP:
        newY = this.y  - this.speed;
        if(newY - this.radius - WALL_WIDTH > 0){
            this.y = newY;
        }
        break;

        case DOWN:
        newY = this.y + this.speed;
        if(newY + this.radius + WALL_WIDTH < CANVAS_HEIGHT) {
            this.y = newY;

        }
        break;


        case LEFT:
        newX = this.x - this.speed;
        if(newX - this.radius - WALL_WIDTH > 0 ){
            this.x = newX;
        }
        break;

        case RIGHT:
        newX = this.x + this.speed;

        if(newX + this.radius + WALL_WIDTH < CANVAS_WIDTH){
            this.x = newX;
        }
        break;
        
        default:
        break;
    }
};

//make an 180-degree turn
Ghost.prototype.turnBack = function() {
    this.dir = oppositeDir(this.dir);
};

//try to turn(if necessary) and move the ghost
Ghost.prototype.move = function() {
    this.isMoving = !this.isMoving;//so the ghost looks like it's moving
    if(this.isWeak){
        //if weak, reduce speed and make an immediate turn.
        //Ghost starts making random moves until turning back to normal
        this.speed = speed/2;
        if(weakCounter === WEAK_DURATION){
            this.dir = oppositeDir(this.dir);
        }
        if(onGridCenter(this.x, this.y) === false){
            this.moveOneStep();
        }
        else{
            var currGrid = maze[getRowIndex(this.y)][getColIndex(this.x)];
            if(currGrid.gridType === GridConstants.LEFT_TOP_RIGHT){
                this.dir = DOWN;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.TOP_RIGHT_BOTTOM){
                this.dir = LEFT;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.RIGHT_BOTTOM_LEFT){
                this.dir = UP;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.BOTTOM_LEFT_TOP){
                this.dir = RIGHT;
                this.moveOneStep();
            }
            else{
                this.randomMove();
            }

        }

        this.stepCounter++;
    }
    else{
        //normal ghost
        if(this.stepCounter != 0 && this.stepCounter % 2 !=0){
            this.speed = speed/2;
            this.stepCounter = 0;
        }
        else{
            this.speed = speed;
        }
        if(onGridCenter(this.x, this.y) === false){
            this.moveOneStep();
        }
        else{
            // on grid center
            //first check if dead end
            var currGrid = maze[getRowIndex(this.y)][getColIndex(this.x)];
            if(currGrid.gridType === GridConstants.LEFT_TOP_RIGHT){
                this.dir = DOWN;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.TOP_RIGHT_BOTTOM){
                this.dir = LEFT;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.RIGHT_BOTTOM_LEFT){
                this.dir = UP;
                this.moveOneStep();
            }
            else if(currGrid.gridType === GridConstants.BOTTOM_LEFT_TOP){
                this.dir = RIGHT;
                this.moveOneStep();
            }
            else{
                switch(this.color){
                    case RED:
                    //blinky
                    this.blinkyMove();
                    break;

                    case CYAN:
                    case ORANGE:
                    //inky
                    this.inkyMove();
                    break;

                    case PINK:
                    //pinky
                    this.pinkyMove();
                    break;
                }
            }
        }
    }
};

/*======================end ghost====================*/


/*====================Initialization Methods==============*/
function setCanvas() {
    canvas = canvas = document.getElementById(canvasID);
    ctx = canvas.getContext("2d");
}

function initCanvas(width, height){
    if(width===undefined || !(width instanceof Number)){
        width = CANVAS_WIDTH;
    }
    if(height===undefined || !(height instanceof Number)){
        height = CANVAS_HEIGHT;
    }

    ctx = canvas.getContext("2d");

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0 , width, height);

    CANVAS_WIDTH = width;
    CANVAS_HEIGHT = height;
}

// draw maze, print instruction on lower-left corner, show lives on top-right corner
function initMaze() {
    for(var i=0; i<maze.length; i++){
        var oneRow = new Array(CANVAS_WIDTH/GRID_WIDTH);
        maze[i] = oneRow;
    }

    // draw maze without beans
    for( var row = 0; row < CANVAS_HEIGHT/GRID_HEIGHT; row++){
        for(var col = 0; col < CANVAS_WIDTH/GRID_WIDTH; col++){
            var beanType = undefined;
            var newGrid = new Grid(col*GRID_WIDTH, row*GRID_HEIGHT, mazeContent[row][col], beanType);
            
            maze[row][col] = newGrid;
            newGrid.draw();
        }
    }

    // write beans
    for(var i=0; i < beanPositions.length; i++){
        var x = beanPositions[i][1];
        var y = beanPositions[i][0];
        maze[x][y].beanType = NORMAL_BEAN;
        maze[x][y].draw();
    }

    // draw power beans
    for(var i=0; i < powerBeanPositions.length; i++){
        var x = powerBeanPositions[i][1];
        var y = powerBeanPositions[i][0];
        maze[x][y].beanType = POWER_BEAN;
        maze[x][y].draw();
    }
}

/*================END Initialization Methods==============*/


/*====================Util Methods================*/
//draw a circle
function circle(ctx, cx, cy, radius) {

    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, 2*Math.PI, true);
    ctx.fill();

}

//get opposite direction
function oppositeDir (dir) {
    switch(dir){
        case UP:
        return DOWN;
        break;

        case DOWN:
        return UP;
        break;

        case LEFT:
        return RIGHT;
        break;

        case RIGHT:
        return LEFT;
        break;

        default:
        return -1;//err
    }
}

function getRowIndex (yCord) {
    if(yCord === undefined){
        return -1;//err
    }
    return parseInt(yCord/GRID_HEIGHT);
}


function getColIndex (xCord) {
    if(xCord === undefined){
        return -1;//err
    }
    return parseInt(xCord/GRID_WIDTH);
}

function sleep(ms)
{
    var dt = new Date();
    dt.setTime(dt.getTime() + ms);
    while (new Date().getTime() < dt.getTime());
}

function fixGrids (x, y) {
    var row = getRowIndex(y);
    var col = getColIndex(x);

    try {
        if(xOnGridCenter(y)){
            maze[row][col].draw();
            if(col+1 < maze.length && !staticArrayContains([row, col+1])){
                maze[row][col+1].draw();
            }
            if(col-1 >= 0 && !staticArrayContains([row, col-1])){
                maze[row][col-1].draw();
            }
        }
        else if(yOnGridCenter(x)){
            maze[row][col].draw();
            if(row+1 < maze.length  && !staticArrayContains([row+1, col])){
                maze[row+1][col].draw();
            }
            if(row-1 >=0 && !staticArrayContains([row-1,col]) ){
                maze[row-1][col].draw();
            }
        }
    } catch(err) {
        console.log('error drawing' + err.message + ', maze dims are ' + maze.length + '/' + maze[0].length)
    }
}

function staticArrayContains(cord) {
    var x = cord[0];
    var y = cord[1];
    for(var i=0; i< staticGrids.length; i++ ){
        if(x=== staticGrids[i][0] &&
            y=== staticGrids[i][1]){
            return true;
        }
    }
    return false;
}

function ghostHouseContains(cord) {
    var x = cord[0];
    var y = cord[1];
    for(var i=0; i< ghostHouse.length; i++ ){
        if(x=== ghostHouse[i][0] &&
            y=== ghostHouse[i][1]){
            return true;
        }
    }
    return false;
}

function onGridCenter (x,y) {
    return xOnGridCenter(y) && yOnGridCenter(x);
}

function xOnGridCenter (y) {
    return ((y - GRID_WIDTH/2) % GRID_WIDTH) === 0;
}

function yOnGridCenter (x) {
    return ((x - GRID_HEIGHT/2) % GRID_HEIGHT) === 0;
}

//see if sprite can move one more step at the given (x,y) facing the given direction
function canMove (x,y,dir) {
    if(!onGridCenter(x,y)){
        return true;
    }
    var canMove = false;
    var currGrid = maze[getRowIndex(y)][getColIndex(x)];
    var gridType = currGrid.gridType;
    switch(dir){
        case UP:
        if(gridType !=GridConstants.LEFT_TOP && gridType !=GridConstants.RIGHT_TOP && gridType !=GridConstants.TOP_BOTTOM
            && gridType !=GridConstants.TOP_ONLY && gridType!=GridConstants.LEFT_TOP_RIGHT 
            && gridType !=GridConstants.TOP_RIGHT_BOTTOM && gridType!=GridConstants.BOTTOM_LEFT_TOP){
            canMove = true;
        }
        break;

        case DOWN:
        if(gridType !=GridConstants.LEFT_BOTTOM && gridType !=GridConstants.TOP_BOTTOM && gridType !=GridConstants.RIGHT_BOTTOM
            && gridType !=GridConstants.BOTTOM_ONLY && gridType!=GridConstants.RIGHT_BOTTOM_LEFT
            && gridType !=GridConstants.BOTTOM_LEFT_TOP && gridType!=GridConstants.TOP_RIGHT_BOTTOM){
            canMove = true;
        }
        break;

        case LEFT:
        if(gridType !=GridConstants.LEFT_BOTTOM && gridType !=GridConstants.LEFT_TOP && gridType !=GridConstants.LEFT_ONLY
            && gridType !=GridConstants.LEFT_RIGHT && gridType!=GridConstants.LEFT_TOP_RIGHT
            && gridType !=GridConstants.BOTTOM_LEFT_TOP && gridType!=GridConstants.RIGHT_BOTTOM_LEFT){
            canMove = true;
        }
        break;

        case RIGHT:
        if(gridType !=GridConstants.RIGHT_BOTTOM && gridType !=GridConstants.RIGHT_TOP && gridType !=GridConstants.RIGHT_ONLY
            && gridType !=GridConstants.LEFT_RIGHT && gridType!=GridConstants.RIGHT_BOTTOM_LEFT 
            && gridType !=GridConstants.TOP_RIGHT_BOTTOM && gridType !=GridConstants.LEFT_TOP_RIGHT){
            canMove = true;
        }
        break;
        default:
        break;
    }
    return canMove;
}
/*=================END Util Methods================*/


/*=================UI Update Methods===============*/

// draw instructions
function printInstruction () {
    ctx.fillStyle = "white";
    ctx.font="12px monospace";
    ctx.textAlign = "left";

    var txt = "WELCOME TO \nPACMAN 15-237!\n\n\nArrow keys or\nWASD to move\n\nQ to pause\nE to resume\nR to restart";
    var x = 12;
    var y = CANVAS_HEIGHT-200;
    var lineheight = 15;
    var lines = txt.split('\n');

    for (var i = 0; i<lines.length; i++)
        ctx.fillText(lines[i], x, y + (i*lineheight) );

    if (ghosts.length === 0){
        ctx.fillStyle = "black";
        ctx.fillRect(x, CANVAS_WIDTH-40, 70, 30);
        ctx.fillStyle = "red";
        ctx.font = "16px monospace";
        ctx.textAlign = "left";
        ctx.fillText("GOD MODE", x, CANVAS_WIDTH-20);
    }

}

//draw lives on top-right corner
function showLives(){
    ctx.fillStyle="black";
    ctx.fillRect(CANVAS_WIDTH-80, 10, 70, 30);
    for(var i=0; i<life-1; i++){
        lives[i] = new Pacman(CANVAS_WIDTH-50+25*i, 30, RIGHT);
        lives[i].draw();
    }
}

//show || update score
function showScore(){
    ctx.fillStyle="black";
    ctx.fillRect(CANVAS_WIDTH-250, 10, 190, 40);
    ctx.fillStyle = "white";
    ctx.font = "24px monospace";
    ctx.textAlign = "left";
    ctx.fillText("score: " + parseInt(score), CANVAS_WIDTH-250, 37);
}

//show win message
function winMessage(){
    //draw popup
    ctx.fillStyle = "black";
    ctx.strokeStyle = "green";
    ctx.lineWidth=5;
    ctx.fillRect(CANVAS_WIDTH/2-150, CANVAS_HEIGHT/2-40, 300, 100);
    ctx.strokeRect(CANVAS_WIDTH/2-150, CANVAS_HEIGHT/2-40, 300, 100);

    //write message
    ctx.textAlign="center";
    ctx.fillStyle = "white";
    ctx.font = "16px monospace";
    ctx.fillText("Congratulations, you won!", CANVAS_HEIGHT/2, CANVAS_HEIGHT/2+6);
    ctx.font = "12px monospace";
    ctx.fillText("press R to play again", CANVAS_HEIGHT/2, CANVAS_HEIGHT/2+28);
}

//show lose message
function loseMessage(){
    //draw popup
    ctx.fillStyle = "black";
    ctx.strokeStyle = "red";
    ctx.lineWidth=5;
    ctx.fillRect(CANVAS_WIDTH/2-100, CANVAS_HEIGHT/2-40, 200, 100);
    ctx.strokeRect(CANVAS_WIDTH/2-100, CANVAS_HEIGHT/2-40, 200, 100);

    //write message
    ctx.textAlign="center";
    ctx.fillStyle = "red";
    ctx.font = "26px monospace";
    ctx.fillText("GAME OVER", CANVAS_HEIGHT/2, CANVAS_HEIGHT/2+7);
    ctx.font = "12px monospace";
    ctx.fillText("press R to play again", CANVAS_HEIGHT/2, CANVAS_HEIGHT/2+28);
}

//update canvas for each frame. 
function updateCanvas() {
    // restartTimer++;
    // if (gameOver()===true){
    //     life--;
    //     // mrPacman.dieAnimation();
    //     showLives();
    //     if (life>0){
    //         sleep(500);
    //         clearInterval(intervalId);
    //         fixGrids(mrPacman.x, mrPacman.y);
    //         for(var i=0; i<ghosts.length; i++){
    //             fixGrids(ghosts[i].x, ghosts[i].y);
    //         }
    //         run();  
    //     }
    //     else {
    //         clearInterval(intervalId);
    //         sleep(500);
    //         loseMessage();
    //     }
        
    // }
    // else if (pacmanWon()===true){
    //     clearInterval(intervalId);
    //     sleep(500);
    //     winMessage();
    // }
    // else{
    //     if(weakCounter>0 && weakCounter<2000/timerDelay){
    //         for(var i=0; i<ghosts.length; i++){
    //             ghosts[i].isBlinking = !ghosts[i].isBlinking;
    //         }
    //     }
    //     if(weakCounter>0){
    //         weakCounter--;
    //     }
    //     if(weakCounter===0){
    //         for(var i=0; i<ghosts.length; i++){
    //             ghosts[i].isDead = false;
    //             ghosts[i].isWeak = false;
    //             ghosts[i.isBlinking = false];
    //             weakBonus= 200;
    //         }
    //     }

    //     eatBean();
    //     eatGhost();
    //     mrPacman.move();

    //     for(var i=0; i<ghosts.length; i++){
    //         if(ghosts[i].isDead === false){
    //             ghosts[i].move();
    //         }
    //     }
    fixGrids(mrPacman.x, mrPacman.y);

    for(var i=0; i<ghosts.length; i++){
        fixGrids(ghosts[i].x, ghosts[i].y);
    }
    
    for(var i=0; i<ghosts.length; i++){
        ghosts[i].draw();
    }
    mrPacman.draw();
}


//try to eat a weak ghost
function eatGhost () {
    for(var i=0; i<ghosts.length; i++){
        if(Math.abs(mrPacman.x-ghosts[i].x)<=5 && Math.abs(mrPacman.y-ghosts[i].y)<=5
            && ghosts[i].isWeak && !ghosts[i].isDead){
            score += parseInt( weakBonus);
            weakBonus *=2;
            showScore();
            ghosts[i].isDead = true;
            ghosts[i].toGhostHouse();
        }
    }
}

function gameOver(){
    for(var i=0; i<ghosts.length; i++){
        if(Math.abs(mrPacman.x-ghosts[i].x)<=5 && Math.abs(mrPacman.y-ghosts[i].y)<=5
            && !ghosts[i].isWeak){
            return true;
        }
    }
    return false;
}

function pacmanWon(){
    return beansLeft === 0;
}
/*==================END UI Update Methods================*/


// accessor functions

function setMaze(_maze) {
    mazeContent = _maze;
    CANVAS_WIDTH = _maze[0].length * GRID_WIDTH
    CANVAS_HEIGHT = _maze.length * GRID_HEIGHT
    maze = new Array(CANVAS_HEIGHT / GRID_HEIGHT);
    console.log('setting new maze of size' + CANVAS_WIDTH + '/' + CANVAS_HEIGHT)
}

function setPowerBeans(powerbeanpos) {
    powerBeanPositions = powerbeanpos;
}

function setBeans(beanpos) {
    beanPositions = beanpos;
}

function placePacman (x, y, dir) {
    if (mrPacman===undefined) {
        mrPacman = new Pacman(x, y, dir);
    } else {
        // clean up
        fixGrids(mrPacman.x, mrPacman.y);
        // draw new
        mrPacman.x = x;
        mrPacman.y = y;
        mrPacman.dir = dir;
    };
}

function placeGhost (i, x, y, col, dir, scared, blinking) {
    if (i >= ghosts.length) {
        ghosts.push(new Ghost(x, y, col, dir));
    } else {
        fixGrids(ghosts[i].x, ghosts[i].y);
        ghosts[i].x = x;
        ghosts[i].y = y;
        ghosts[i].dir = dir;
        ghosts[i].isWeak = scared ? scared : false;
        ghosts[i].isBlinking = blinking ? scared : false;
    };
}
/*===============END Game Control Methods===================*/

function startGame() {intervalId = setInterval(updateCanvas, 50);};
function stopGame() {clearInterval(intervalId)};

function removeBean(x, y) { maze[y][x].beanType = undefined;} 
/*-----------GAME START-----------*/
// initFields();
// initCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
// canvas.addEventListener('keydown', onKeyDown, false);
// canvas.setAttribute('tabindex','0');
// canvas.focus();

exports.setCanvas = setCanvas
exports.initCanvas = initCanvas
exports.canvas = canvas
exports.intervalId = intervalId
exports.clearInterval = clearInterval
exports.initMaze = initMaze
exports.setMaze = setMaze
exports.setPowerBeans = setPowerBeans
exports.setBeans = setBeans
exports.placePacman = placePacman
exports.placeGhost = placeGhost
exports.startGame = startGame
exports.stopGame = stopGame
exports.removeBean = removeBean
});
