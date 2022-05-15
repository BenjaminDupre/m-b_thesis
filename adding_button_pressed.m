% Example 
i=11
all = all2(i).data
% Visualization of the problem.
tiledlayout(3,1)
ax1 = nexttile;
plot(all2(11).data.time,all2(11).data.buttonHasBeenPressed,all2(11).data.time,categorical(A(:,5)),all2(11).data.time,all2(11).data.buttonCurrentlyPressed)
ax2 = nexttile;
plot(ax2,all2(11).data.time,all2(11).data.levelCounter,'p')
ax3=nexttile;
plot(ax3,all2(11).data.time,all2(11).data.set,'b')
% Second Visualization of the Problem
tiledlayout(2,1)
ax1 = nexttile;
plot(all2(11).data.time,categorical(all2(11).data.levelCounter),all2(11).data.time,categorical(A(:,5)*35),all2(11).data.time,categorical(all2(11).data.buttonHasBeenPressed))
ax2 = nexttile;
plot(all2(11).data.time,all2(11).data.buttonHasBeenPressed)

% Looking into additional variables: Explosionis Trigered -  Makes no sense
[x.eT, y.eT, z.eT] = vr_p2double(string(all.isExplosionTriggered));
plot3(x.eT, y.eT, z.eT)

% Solution
%B=[];
for r = 2:height(all)
    A(r,1) = all.set(r-1)~=all.set(r);
    A(r,2) = all.levelCounter(r-1)~=all.levelCounter(r);
    A(r,3) = all.buttonCurrentlyPressed(r-1)~=all.buttonCurrentlyPressed(r);
    A(r,4) = all.buttonHasBeenPressed(r-1)~=all.buttonHasBeenPressed(r);
    A(r,5) = all.redBallPosition(r-1)~=all.redBallPosition(r);   
end
% Try 
for r = 2:height(all)
    A(r,1) = all.set(r-1)~=all.set(r);
    A(r,2) = all.levelCounter(r-1)~=all.levelCounter(r);
    A(r,3) = all.buttonCurrentlyPressed(r-1)~=all.buttonCurrentlyPressed(r);
    A(r,4) = all.buttonHasBeenPressed(r-1)~=all.buttonHasBeenPressed(r);
    A(r,5) = all.redBallPosition(r-1)~=all.redBallPosition(r);   
end
    
for set = 1:3
    for lvl=0:1:35
        if height(unique(all(all.levelCounter==lvl & all.set==set,"buttonCurrentlyPressed")))>=2
            fprintf("Button pressed in lvl %d - set %d \n",lvl,set)
            if height(unique(all(all.levelCounter==lvl-1 & all.set==set,"buttonCurrentlyPressed")))>=2
                fprintf("Previously Pressed - Normal way to Start in lvl %d - set %d \n",lvl,set)
            else
                fprintf("Take the second ball move or change in Button have been pressed in lvl %d - set %d \n",lvl,set)
            end
        else
            fprintf("Normal way to Start lvl in lvl %d - set %d \n",lvl,set)
        end
    end
end



 A.Properties.VariableNames = {'set' 'lvl' 'start' 'end' 'diff'};         % this gives names to columns

[row,col] = find(A==1);                                                     % I use find because I need the row number (instead of inequeality which is faster)
    ver = [array2table(indx) all(indx,'levelCounter') all(indx,'set')]; 
tosee= [row,col],

comparison = hasChanged(all.set)
% Local Functions 
function [x, y, z] = vr_p2double(vr_p)
    pattern = '\(|)'; %removing parenthesis
    vr_p = regexprep(vr_p, pattern, '');
    vr_p = split(vr_p,', ');
    
    x = str2double(vr_p(:,1));
    y = str2double(vr_p(:,2));
    z = str2double(vr_p(:,3));
end
