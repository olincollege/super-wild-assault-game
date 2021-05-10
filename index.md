<div align=center>
<br/>
<img src= "./images/pixel_olin.png"/>
<br/>
<br/>
<section id="downloads">
          <a href="./download" class="btn btn-github"><span class="icon"></span>Play the Game</a>
        </section>
</div>

<br/>
<br/>

## S.W.A.G. is a platform fighter game drawing inspiration from M.U.G.E.N., Super Smash Bros., and Street Fighter. Our goal was to create a configurable engine similar to M.U.G.E.N. that new characters can be added to with relative ease.
<br/>
<br/>
<br/>
<br/>

# **The Engine**: *Create your own character*
- Given the nature of S.W.A.G., anyone is able to create their own characters and add them to the fighting game! Here are the requirements of the characters as you add them in, in their own folder in the `/chars/` folder.
<br/>
<br/>

### Character Information:
`Within the [character].info file, in json style.`
<br/>

1. **Name, Health, Weight, and Physics:**

    - Customize the max health and weight of the character to set the feeling of the way that they move. 
    
    - **Ground physics** include ground acceleration, speed, and traction across the floor of the stage.
    
    - **Aerial physics** include air acceleration, speed, fall speed, and jump acceleration. 
<br/>
<br/>

2. **Moveset Animation Interactions:**
    - **Allowed states**: When the certain character animation can start
    - **Cancelable start**: At what frame the move can be canceled by letting go a key press
    - **Can move**: whether or not a player can go right or left during an animation *(i.e. blocking or jabbing)*.
<br/>
<br/>

### Sprites: Moveset Animations:
`Within the /SPRITES/[move]/ folder.`
<br/>

Add frames for animations for each the moves the character has! Here is the list of moves: **Idle**, **walk**, **jab**, **block**, **air idle**, **jump**, **land**, and got **hit**. When implemented with the *Player* script, this information is immediately utilized by the engine.

<br/>
<div align=center>
<img src= "./images/olinman_idle-1.png"/> <img src= "./images/olinman_idle-2.png"/> <img src= "./images/olinman_idle-4.png"/> <img src= "./images/olinman_idle-5.png"/> <img src= "./images/olinman_idle-7.png"/> <img src= "./images/olinman_idle-8.png"/> <img src= "./images/olinman_idle.gif"/><br/>

<img src= "./images/catboy_walk-1.png"/> <img src= "./images/catboy_walk-3.png"/> <img src= "./images/catboy_walk-5.png"/> <img src= "./images/catboy_walk-7.png"/> <img src= "./images/catboy_walk-9.png"/> <img src= "./images/catboy_walk-11.png"/> <img src= "./images/catboy_walk.gif"/><br/>
</div>
<br/>
<br/>

### Framedata: Hitboxes and Hurtboxes:
`Within the [character].anim file, in CSV style.`
<br/>
Give information about the size and location of these boxes which control the interaction between characters, such as whether or not a player's hit connects with the head and torso, or legs.
- **Hitbox**: Where the player is vulnerable to being hit
- **Hurtbox**: Where contact leads to damage of the opponent
<div align=center>
<img src= "./images/olinman_jab.gif"/> <img src= "./images/catboy_hit.gif"/>
</div>
<br/>
<br/>
<br/>

<div align=center>
<h1> About Us: </h1>
<h2> Jacob Smilg </h2>
<div style= "width:50%"> Class of 2024.<br/>Hates video games.</div>
<br/>
<h2> Melissa Kazazic </h2>
<div style= "width:50%"> Class of 2024.<br/>Jock that shoves people into lockers.</div>
<br/>
<br/>
<img src= "./images/title.png"/>
</div>