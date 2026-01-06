import os
import fastf1
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

track_name = input("Which F1 race do you want to plot? ").strip()

session = fastf1.get_session(2023, track_name, "R")
session.load()

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.set_xlabel('X Position (m)', color='white')
ax.set_ylabel('Y Position (m)', color='white')
ax.set_title("Track Layout", color='white')
ax.tick_params(colors='white') 

num_dots = 20
dot_idx = np.full(num_dots, fill_value=0, dtype=float)

laps = session.laps.sort_values('LapTime').iloc[:num_dots]
pos_list = [laps.iloc[i].get_pos_data() for i in range(num_dots)]

driver_names = [
    "Ham", "Ver", "Lec", "Sai", "Bor",
    "Rus", "Nor", "Alo", "Oco", "Gas",
    "Tsu", "Had", "Ant", "Bea", "Col",
    "Str", "Law", "Pia", "Alb", "Hulk"
]

driver_speeds = {
    "Ham": 2.0, "Ver": 2.2, "Lec": 1.8, "Sai": 1.7,
    "Bor": 1.9, "Rus": 1.85, "Nor": 1.75, "Alo": 1.6,
    "Oco": 1.5, "Gas": 1.55, "Tsu": 1.5, "Bea": 1.65,
    "Ant": 1.6, "Had": 1.5, "Law": 1.45, "Str": 1.55,
    "Alb": 1.5, "Pia": 1.4, "Col": 1.35, "Hulk": 1.3
}

speed = np.array([driver_speeds[name] for name in driver_names], dtype=float)

colors = plt.get_cmap('tab20', num_dots)

ax.plot(pos_list[0]['X'], pos_list[0]['Y'], color='white', linewidth=2, linestyle='--')

dots = []
labels = []

for i in range(num_dots):
    d, = ax.plot(
        pos_list[i]['X'].iloc[0],
        pos_list[i]['Y'].iloc[0],
        'o',
        markersize=5,
        color=colors(i)
    )
    dots.append(d)
    
    label = ax.text(
        pos_list[i]['X'].iloc[0],
        pos_list[i]['Y'].iloc[0],
        driver_names[i], 
        color=colors(i),
        fontsize=8,
        ha='left',
        va='bottom'
    )
    labels.append(label)

def init():
    for i in range(num_dots):
        x0 = pos_list[i]['X'].iloc[0]
        y0 = pos_list[i]['Y'].iloc[0]
        dots[i].set_data([x0], [y0])
        labels[i].set_position((x0, y0))
    return list(dots) + list(labels)

delay_frames = 60

def update(frame):
    global dot_idx

    if frame < delay_frames:
        return list(dots) + list(labels)

    for i, dot in enumerate(dots):
        dot_idx[i] = (dot_idx[i] + speed[i]) % (len(pos_list[i])-1)

        idx_floor = int(dot_idx[i])
        idx_ceil = (idx_floor + 1) % len(pos_list[i])
        t = dot_idx[i] - idx_floor

        x = pos_list[i]['X'].iloc[idx_floor]*(1-t) + pos_list[i]['X'].iloc[idx_ceil]*t
        y = pos_list[i]['Y'].iloc[idx_floor]*(1-t) + pos_list[i]['Y'].iloc[idx_ceil]*t

        dot.set_data([x],[y])
        labels[i].set_position((x, y))

    return list(dots) + list(labels)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=max(len(p) for p in pos_list) + delay_frames,
    interval=100,
    blit=True
)

plt.show()
