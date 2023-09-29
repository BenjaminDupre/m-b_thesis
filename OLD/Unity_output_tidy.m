tic
% Author : Benjamin Dupré
% Raw Data Prep & Wrangling for Analysis

%% Defining Working Space and Participant Iteration.  
%allFolder = ['C:\Users\dupre\Dropbox\My Mac (glaroam2-185-117.wireless.' ...                                                                      
%    'gla.ac.uk)\Documents\Research MaxPlank\P1_propioception\' ...                                                                                  
%    'Data_Wrangling\Matlab Analysis\Data_Wrangling\'];                      % Location of raw data 
allFolder = '/Users/benjamin/Documents/Data_Wrangling/';
cd(allFolder)                                                               % making allFolder the working directory. 

parti = dir(allFolder);                                                     % Selecting 
parti(~[parti.isdir]) = [];                                                 % Filters out all that are not directories
tf = ismember( {parti.name}, {'.','..','__MACOSX'});                        % Filters out the parent and current directory '.' and '..'
parti(tf) = [];                                                             % Filters out the parent and current directory '.' and '..'
numberOfFolders = length(parti);                                            % Geting the number of participants and length of iteration                                          
%all2(5).ptcp = [];                                                          % preallocating space 
all_behavioral = [];
%%% ==============Iteration for every Participant.==============
%all2 =cell(1,22);                                                           % preallocate for known total of participants.!!!CREATS ERROR 
for i=numberOfFolders:-1:1
    
    ptcp=parti(i).name;
    all2(i).ptcp = ptcp;
        
    % Setup the Import Options and import the data    

        % function all= importdata(,) Trying to make a function to make it
        % faster - no succes atm. 
        opts = delimitedTextImportOptions("NumVariables", 28);
        
        % Specify range and delimiter
        opts.DataLines = [100, Inf];
        opts.Delimiter = ";";
        
        % Specify column names and types
        opts.VariableNames = ["time", "Milliseconds",...
            "levelCounter", "correctCounter",...
            "leftHandPosition", "leftHandRotation",...
            "rightHandPosition", "rightHandRotation", ...
            "redBallPosition", "redBallRotation",...
            "leftHandGrab", "rightHandGrab", "feedbackType", ...
            "leftHandVibration", "rightHandVibration", ...
            "correctBallPosition", "lastTemplateBallPosition",...
            "areCalibratingGhostHandsActive",...
            "areGrabbingGhostHandsActive", "calibrationState",...
            "isCalibrationBlocked", "grabbingState", ...
            "buttonHasBeenPressed", "buttonCurrentlyPressed",...
            "headPosition", "headRotation", "isExplosionTriggered", "ECG"];
        opts.VariableTypes = ["datetime", "double", "double", "double",...
            "string", "string", "string", "string", "string", ...
            "categorical", "categorical", "categorical", "categorical", ...
            "categorical", "categorical", "categorical", "categorical",...
            "categorical", "categorical", "categorical", "categorical",...
            "categorical", "categorical", "categorical", "categorical",...
            "categorical", "categorical", "double"];
        
        % Specify file level properties
        opts.ExtraColumnsRule = "ignore";
        opts.EmptyLineRule = "read";
        
        % Specify variable properties
        opts = setvaropts(opts, ["leftHandPosition", "leftHandRotation", ...
            "rightHandPosition", "rightHandRotation", "redBallPosition",...
            "redBallRotation", "leftHandGrab", "rightHandGrab",...
            "feedbackType", "leftHandVibration", "rightHandVibration",...
            "correctBallPosition", "lastTemplateBallPosition",...
            "areCalibratingGhostHandsActive", "areGrabbingGhostHandsActive",...
            "calibrationState", "isCalibrationBlocked", "grabbingState",...
            "buttonHasBeenPressed", "buttonCurrentlyPressed",...
            "headPosition", "headRotation", "isExplosionTriggered"],...
            "EmptyFieldRule", "auto");
        opts = setvaropts(opts, "time", "InputFormat", "yyyy-MM-dd HH:mm:ss.SSS");
        opts = setvaropts(opts, "ECG", "TrimNonNumeric", true);
        opts = setvaropts(opts, "ECG", 'DecimalSeparator', ",");
        
        % Define Work Space by Participant For Every Set. 
        % This preallocates space
        %mainFolder = fullfile('C:', 'Users', 'dupre', 'Dropbox', ...
        %    'My Mac (glaroam2-185-117.wireless.gla.ac.uk)', 'Documents',...
        %    'Research MaxPlank','P1_propioception', 'Data_Wrangling',...
        %    'Matlab Analysis', 'Data_Wrangling', ptcp);                     % Opens Participants Folder
        
        mainFolder = fullfile(allFolder, ptcp); 

        subdirs = dir(mainFolder);                                          % Shows all availables 
        subdirs(~[subdirs.isdir]) = [];                                     % This filters out all the items in the main folder that are not directories
        tf = ismember( {subdirs.name}, {'.','..','__MACOSX'});              % And this filters out the parent and current directory '.' and '..'
        subdirs(tf) = [];
        numberOfFolders = length(subdirs);
        
        % Imports 'everything' and paste after or the 3 sets done 
        all= [];   
        for j=1:numberOfFolders                                             % this is to go through every folder 
            thissubdir = subdirs(j).name;
            subdirpath = join([mainFolder filesep thissubdir],'');
            data = readtable([subdirpath  filesep 'everything.csv'], opts);
            data.set = ones(height(data),1)*j; % Creates varaible Set with the number of Set
            all = [all ; data];
        end
        
        
    clear opts data j subdirpath tf thissubdir subdirs mainFolder           % Clear temporary variables from data import.
    
    all = rmmissing(all);                                                   % removes missing variables. 

    all2(i).data = all;                                                     % Saves all into data structure. 


    % Building response time
    % FINDING START1 (finding when the ball is placed in the hand). 
    % into either the left or right hand. Looking for behavioral data ball
    % position. % Here level 35 is found with no start. 
    % This is because it is a limit level. 
    % From here we consider 35 levels only (remember we star at 0).
    B=[];    
    for set = 1:3
        for lvl=0:1:35
            meanwhile=all(all.levelCounter==lvl & all.set==set,:);
            if height(unique(meanwhile(:,"buttonCurrentlyPressed")))>=2 && height(unique(all(all.levelCounter==lvl-1 & all.set==set,"buttonCurrentlyPressed")))<2
                fprintf("Button pressed in lvl %d - set %d need to go for following change of ball position\n",lvl,set)
                A = zeros(height(meanwhile)-1,1); 
                A2= zeros(height(meanwhile)-1,1);
                A3= zeros(height(meanwhile)-1,1);            
                for r = 2:height(meanwhile)
                    if sum(A)<1                                                 % going through all observations one level at a time. 
                        A(r,1) = (meanwhile.buttonHasBeenPressed(r-1)=="TEMPLATE_IS_ACTIVE" & meanwhile.buttonHasBeenPressed(r)=='AFTER_TEMPLATE_IS_ACTIVE');       % through one i the ball changes position. 
                    else 
                        A2(r,1) = (meanwhile.buttonHasBeenPressed(r-1)=="TEMPLATE_IS_ACTIVE" & meanwhile.buttonHasBeenPressed(r)=='AFTER_TEMPLATE_IS_ACTIVE');
                        if sum(A2)>= 1       
                                A3(r,1)  = meanwhile.redBallPosition(r-1)~=meanwhile.redBallPosition(r);
                                break
                        end
                        
                    end
                end
                A=[0;A3];
                clear A2 A3
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
    clear meanwhile
    indx = find(B(:,1)==1);                                                 % I use find because I need the row number (instead of inequeality which is faster)
    ver = [array2table(indx) all(indx,'levelCounter') all(indx,'set')];     % merging row_start level_counter and set
    
    START = [];                                                             % merging level, set and start into one table
    for j = min(all.set):max(all.set)                                          
        for k = min(ver.levelCounter):max(ver.levelCounter)                 % for every level consider the changes ball position only
            sub_vect = ver(ver.set==j & ver.levelCounter==k,:);             % for every level save the first change in ball position.
            if height(sub_vect)<1
                sub_vect(1,:)= table(["no start"],[k],[j]);
            end
            START = [START ;sub_vect(1,:)];                                 % this part puts all the starts for every set and level into one long table.
        end
    end
    clear A B r indx ver j k F ver2 sub_vect



    % Finding END
    % This is the ending we finally opted for. When the game the collider explotes
    % the trial ends. Is not poluted by the push black
    % button cases, niether the if the ball felt from the board. The cases that
    % participant drop the ball over the table and made into the board
    % under 6!!! would still be included. ( I dont know how many of those?)

    A = zeros(height(all)-1,1);
    for r = 1:height(all)-1                                                 % going through all observationthorugh one level at the time
        A(r,1) = all.levelCounter(r+1)~=all.levelCounter(r);                % registers the moment the level changes 
        %A(r,2) = all.set(r);                                               % this adds the matrix the set value 
        %A(r,3) = all.levelCounter(r);                                      % this adds to the matrix the level counter value
    end
    indx = find(A(:,1)==1);
    ver = [array2table(indx) all(indx,'levelCounter') all(indx,'set')];
    %END2 = array2table([indx A(indx,:); 0 0 0 0], 'VariableNames',{'id' 'TorF' 'set' 'lvl'});


    clear A indx r 


    % Creating one table with starts and stops and feedbacktype and correct answers. 
    bhv = [];
    for set = 1:3
        for r = 0:34
             meanwhile = table(set, r, table2array(START(START.levelCounter==r & START.set ==set,1)), table2array(ver(ver.levelCounter==r & ver.set ==set,1)));
             bhv = [bhv;meanwhile];
        end 
    end 
    %table2array(ver(:,"levelCounter")),==table2array(START1(:,"levelCounter"))

    bhv.diff = bhv{:,4} - bhv{:,3};                                         % this creates a diff column between start and end
    bhv.diff = bhv.diff/133;                                                % this getting diff column into seconds
    bhv.Properties.VariableNames = {'set' 'lvl' 'start' 'end' 'diff'};      % this gives names to columns
    % bhv.stimulus = all_lvl.stimulus LEAVING STIMULUS COLUMN OUT!
    
    bhv(bhv.diff <= 0 | bhv.diff > 11 ,:)=[];                               % removing outliers 
    B= bhv;                                                                 % creating instrumental varaible
    r_time.data = B;
    all2(i).rtime = r_time;
    clear pd M h p ci stats bhv all_lvl END2 START1 START ver 


    %%% ============== Adding mistakes =========================================
    %mistakes=[];                                                           % this creates intrumental matrix
    mistakesf=[];                                                           % this creates goal matrix
    behavioral_b = [];                                                      % this creates the behavioral with times+mistakes                 
    
    A = zeros(size(all,1)-1,4);                                            % this preallocates space for all data
    for line=1:size(all,1)-1                                               % this indicates to go over every row
        A(line,3) = all.correctCounter(line+1)~=all.correctCounter(line);  % this looks for diferences in correct counter
        A(line,1) = all.set(line);                                         % this adds to A the set number 
        A(line,2) = all.levelCounter(line);                                % this ads the level counter
        A(line,4) = all.feedbackType(line);                                % this adds the feedback the the moment
    end
    
    indx = find(A(:,3)==1);                                                 % this gets the exact moment where the correct changed 
    A = A(indx,:);
    mistakes = [A(diff(A(:,2))>1,:) i*ones(size(A(diff(A(:,2))>1,:),1),1) ];
    mistakesf = [mistakesf; mistakes];
   
    clear A 

    mistakesf(:,2) = mistakesf(:,2)+1;                                      % this goes back to the exact level nummber where the mistake was done.
    mistakes_ag = array2table(mistakesf, 'VariableNames',{'set',...
        'level','mistake','stimuli','participant'});                        % this adds names 
    
    clear line mistakes mistakesf indx

        behavioral_a =[];
        responsetime = all2(i).rtime.data;
        responsetime.ptcp = ones(size(all2(i).rtime.data,1),1)*i;
        behavioral_a = [behavioral_a;responsetime ];
    
    for l=1:size(mistakes_ag,1)                                             % It uses variable mistakes_ag to add a variable that has a value one when 
        behavioral_a.accuracy(behavioral_a.ptcp == ...                      % the ball is placed in the wrong hold.
        mistakes_ag.participant(l)&...
        behavioral_a.set == mistakes_ag.set(l)&...
        behavioral_a.lvl == mistakes_ag.level(l),:)=1;
    end
    behavioral_b = [behavioral_b; behavioral_a ];
    clear responsetime l behavioral_a
       
    %% Registering  mistakes and error in loaded participant data 
    if size(categories(all.feedbackType),1)>3                           % If there are more than three conditions then write in file 
        fileID = fopen(['/Users/benjamin/Documents/GitHub/m-b_thesis' filesep...
            'verzeichnis.txt'],'a');
        fprintf(fileID,['too many categories in ' ptcp ...
            ', removing excess categories \n']);
        fclose(fileID);
        all2(i).data.feedbackType = removecats(all.feedbackType);       % this fucntion removes the weak conditions 
        all.feedbackType = removecats(all.feedbackType);                % This is the same but with a instrumental variable ???                                                      
    end
    clear fileID ans
    %%% ==============  Gets the number of observation feedtype per level.
    a  = groupcounts(all,{'set', 'levelCounter', 'feedbackType'});      % groups data into set, level and condition
    a = a(a.GroupCount>276,:);                                          % elimine the rows within the two second overlap from the previous condition is not the new one
    % Labeling each level with one feedtype by aplying it to the 
    % maximun.
    all_lvl = [];
    for j=1:max(all.set)                                                % size(all2,2)
        b = a(a.set==j,:);                                              % this subset for set
        lvl = array2table([unique(b.levelCounter), ...
            zeros(height(unique(b.levelCounter)),1)],'VariableNames', ...
            {'level' 'stimulus'});                                      % this predefines the table we wannt to build (it adds one finishing in 36 )
        for r =min(b.levelCounter):max(b.levelCounter)                  % this make it go for every level. 
            opt = b(b.levelCounter == r,:);                             % this makes the instrumental variable only consider one set at a time
            if height(opt) > 1                                          % this allows to if there is more than one level to continue
                Idx = find(opt.GroupCount == max(opt.GroupCount),1);    % this assigns the labels of the feedbacktype with the most observations to the complete level (basicly i am  assigning the most counted condition )
                lvl(r+1,2) = table(opt.feedbackType(Idx,:));            % this insert the value rescued from the previous step.
            else
            lvl(r+1,2) = table(opt.feedbackType);                       % this directly assign the only stimulus possible for the level
            end
        end
        c = [table(ones(max(b.levelCounter)+1,1)*j,'VariableNames',...
            {'set'}) lvl];                                              % this codes adds a first column with the set number
        all_lvl = [all_lvl; c];
    end
    % adding the feedbacktype to the stimulus
    for z=min(behavioral_b.set):max(behavioral_b.set)
        for y=min(behavioral_b.lvl):max(behavioral_b.lvl)
        behavioral_b(all_lvl.set==z & all_lvl.level==y,8) = all_lvl(all_lvl.set==z & all_lvl.level==y,3);
        end
    end
    clear z y
    behavioral_b.Properties.VariableNames{'Var8'} = 'Stimulus';

    % Getting level with problems and saving them in a file 

        for j= min(a.set):max(a.set)
             b = a(a.set==j,:);                                            % this subsamples to one set the table
             d = groupcounts(all_lvl(all_lvl.set==j,:),'stimulus');
             if d.GroupCount ~= 12    
                for r = min(b.levelCounter):max(a.levelCounter)             % this makes the checks for every level of the set
                    opt = b(b.levelCounter == r,:);
                    if height(opt)>1 & abs(diff(opt.GroupCount)) < 400
                        fileID = fopen(['/Users/benjamin/Documents/GitHub/m-b_thesis' ...
                            filesep 'count_condition.txt'],'a');
                        fprintf(fileID,...
                            "Problem for %s in level %d. set %d. Condition:" + ...
                            "Difference under 400\n",ptcp,r,j) ;
                        fclose(fileID);
                    elseif height(opt)>1 && sum(opt.GroupCount) > ...
                            max(b.GroupCount)-0.1*max(b.GroupCount)
                        fileID = fopen(['/Users/benjamin/Documents/GitHub/m-b_thesis' ...
                            filesep 'count_condition.txt'],'a');
                        fprintf(fileID,...
                            "Problem for %s in level %d. set %d. Condition:" + ...
                            "Too long period Sum \n",ptcp,r,j) ;
                        fclose(fileID);
                    end
                end
           else
                fprintf("Alles gut \n Gleich Anzahl von Fällen an einstellen %d \n ",j);
           end
       end
       % Ading participant name column 
       behavioral_b.ptcp = repmat(ptcp, height(behavioral_b), 1); 
       % Also saving al into one behavioral object 
       all_behavioral = [all_behavioral; behavioral_b] ; 
        % Clear all and close
        clear d  b c Idx j sset r a opt fileID
        

    
end
saveFolder = '/Users/benjamin/Documents/GitHub/m-b_thesis'; %'C:\Users\dupre\Documents\GitHub\m-b_thesis\Data';              
writetable(all_behavioral,[saveFolder filesep 'behavior.csv'])
% Getting rid of all instrumental variables.
%clear all_behavioral 
toc



