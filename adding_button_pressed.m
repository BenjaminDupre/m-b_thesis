% Example 
i=11
all = all2(i).data;
% Visualization of the problem. requires using A from Solution 1 in line 25
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
% / Can make use off this variable
[x.eT, y.eT, z.eT] = vr_p2double(string(all.isExplosionTriggered));
plot3(x.eT, y.eT, z.eT)

% Solution 1
%B=[];
for r = 2:height(all)
    A(r,1) = all.set(r-1)~=all.set(r);
    A(r,2) = all.levelCounter(r-1)~=all.levelCounter(r);
    A(r,3) = all.buttonCurrentlyPressed(r-1)~=all.buttonCurrentlyPressed(r);
    A(r,4) = all.buttonHasBeenPressed(r-1)~=all.buttonHasBeenPressed(r);
    A(r,5) = all.redBallPosition(r-1)~=all.redBallPosition(r);   
end


B=[];    
for set = 1:3
    for lvl=0:1:35
        meanwhile=all(all.levelCounter==lvl & all.set==set,:);
        if height(unique(meanwhile(:,"buttonCurrentlyPressed")))>=2 && height(unique(meanwhile(meanwhile.levelCounter==lvl-1,"buttonCurrentlyPressed")))<2
            fprintf("Button pressed in lvl %d - set %d need to go for following change of ball position\n",lvl,set)
            A = zeros(height(meanwhile)-1,1); 
            A2= zeros(height(meanwhile)-1,1);
            A3= zeros(height(meanwhile)-1,1);
            for r = 2:height(meanwhile)
                if sum(A)<1                                                 % going through all observations one level at a time. 
                    A(r,1) = (meanwhile.buttonHasBeenPressed(r-1)=="TEMPLATE_IS_ACTIVE" & meanwhile.buttonHasBeenPressed(r)=='AFTER_TEMPLATE_IS_ACTIVE');       % through one i the ball changes position. 
                else 
                    A2(r,1) = (meanwhile.buttonHasBeenPressed(r-1)=="TEMPLATE_IS_ACTIVE" & meanwhile.buttonHasBeenPressed(r)=='AFTER_TEMPLATE_IS_ACTIVE');
                    if A2>= 1
                            A3(r,1)  = meanwhile.redBallPosition(r-1)~=meanwhile.redBallPosition(r);
                    end
                end
            end
            if height(unique(meanwhile(:,"buttonCurrentlyPressed")))>=2 && height(unique(meanwhile(meanwhile.levelCounter==lvl-1,"buttonCurrentlyPressed")))>=2
               fprintf("Previously Pressed - Normal way to Start in lvl %d - set %d \n",lvl,set)
               A = zeros(height(meanwhile)-1,1);
               for r = 2:height(meanwhile)                                         
                   A(r,1) = meanwhile.redBallPosition(r-1)~=meanwhile.redBallPosition(r); % going through all observations one level at a time. 
               end
           else
            fprintf("Take the second ball move or change in Button have been pressed in lvl %d - set %d \n",lvl,set)
           end
       else
            fprintf("Normal way to Start lvl in lvl %d - set %d \n",lvl,set)
            A = zeros(height(meanwhile)-1,1);
            for r = 2:height(meanwhile)                                                   % going through all observations one level at a time. 
                A(r,1) = meanwhile.redBallPosition(r-1)~=meanwhile.redBallPosition(r);          % through one i the ball changes position. 
            end
       end
        B= [B;A];
    end
end



%% Ubungen 


% Local Functions 
function [x, y, z] = vr_p2double(vr_p)
    pattern = '\(|)'; %removing parenthesis
    vr_p = regexprep(vr_p, pattern, '');
    vr_p = split(vr_p,', ');
    
    x = str2double(vr_p(:,1));
    y = str2double(vr_p(:,2));
    z = str2double(vr_p(:,3));
end

