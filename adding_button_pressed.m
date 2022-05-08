% Example 
i=11
all = all2(i).data
% Visualization of the problem.
tiledlayout(4,1)
ax1 = nexttile;
plot(ax1,all2(11).data.buttonHasBeenPressed,'r')
ax2 = nexttile;
plot(ax2,all2(11).data.buttonCurrentlyPressed,'g')
ax3=nexttile;
plot(ax3,all2(11).data.levelCounter,'p')
ax4=nexttile;
plot(ax4,all2(11).data.set,'b')
% Solution




