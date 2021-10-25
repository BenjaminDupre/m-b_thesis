tic
%% Defining Working Space and Participant Iteration.  
allFolder = ['C:\Users\dupre\Dropbox\My Mac (glaroam2-185-117.wireless.' ...                                                                      
    'gla.ac.uk)\Documents\Research MaxPlank\P1_propioception\' ...                                                                                  
    'Data_Wrangling\Matlab Analysis\Data_Wrangling\'];                      % Location of raw data 
cd(allFolder)                                                               % making allFolder the working directory. 
parti = dir(allFolder);                                                     % Selecting 
parti(~[parti.isdir]) = [];                                                 % Filters out all that are not directories
tf = ismember( {parti.name}, {'.','..','__MACOSX'});                        % Filters out the parent and current directory '.' and '..'
parti(tf) = [];                                                             % Filters out the parent and current directory '.' and '..'
numberOfFolders = length(parti);                                            % Geting the number of participants and length of iteration                                          
%all2(5).ptcp = [];                                                          % preallocating space 
behavioral_b = [];

%%% ==============Iteration for every Participant.==============
for i=1:numberOfFolders
    ptcp=parti(i).name;
    all2(i).ptcp = ptcp;
        
    % Setup the Import Options and import the data    
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
        all= [];                                                            % This preallocates space
        mainFolder = fullfile('C:', 'Users', 'dupre', 'Dropbox', ...
            'My Mac (glaroam2-185-117.wireless.gla.ac.uk)', 'Documents',...
            'Research MaxPlank','P1_propioception', 'Data_Wrangling',...
            'Matlab Analysis', 'Data_Wrangling', ptcp);                     % Opens Participants Folder
        subdirs = dir(mainFolder);                                          % Shows all availables 
        subdirs(~[subdirs.isdir]) = [];                                     % This filters out all the items in the main folder that are not directories
        tf = ismember( {subdirs.name}, {'.','..','__MACOSX'});              % And this filters out the parent and current directory '.' and '..'
        subdirs(tf) = [];
        numberOfFolders = length(subdirs);
        
        % Imports 'everything' and paste after or the 3 sets done 
        for j=1:numberOfFolders                                             % this is to go through every folder 
            thissubdir = subdirs(j).name;
            subdirpath = join([mainFolder filesep thissubdir],'');
            data = readtable([subdirpath  filesep 'everything.csv'], opts);
            data.set = ones(height(data),1)*j; 
            all = [all ; data];
        end
        
        % Clear temporary variables from data import.
        clear opts data j subdirpath tf thissubdir subdirs mainFolder
        all = rmmissing(all);

    all2(i).data = all;                                                     % Saves all into data structure. 
       
        % Checking for mistakes and error in loaded participant data 
        if size(categories(all.feedbackType),1)>3                           % If there are more than three conditions then write in file 
            fileID = fopen(['C:' filesep 'Users' filesep 'dupre' filesep...
                'verzeichnis.txt'],'a');
            fprintf(fileID,['too many categories in ' ptcp ...
                ', removing excess categories \n']);
            fclose(fileID);
            all2(i).data.feedbackType = removecats(all.feedbackType);       % What exactly am I leaving and removing here?
            all.feedbackType = removecats(all.feedbackType);                % This is the same but with a instrumental variable ???                                                      
        end
        clear fileID ans

        % Gets the number of observation feedtype per level.
        a  = groupcounts(all,{'set', 'levelCounter', 'feedbackType'});

        % Labeling each level with one feedtype by aplying it to the 
        % maximun.
        all_lvl = [];
        for j=1:max(all.set)                                                % size(all2,2)
            b = a(a.set==j,:);                                              % this subset for set
            lvl = array2table([unique(b.levelCounter), ...
                zeros(max(b.levelCounter)+1,1)],'VariableNames', ...
                {'level' 'stimulus'});                                      % this predefines the table we wannt to build 
            for r =min(b.levelCounter):max(b.levelCounter)                  % this make it go for every level. 
                opt = b(b.levelCounter == r,:);                             % this makes the instrumental variable only consider one set at a time
                if height(opt) > 1                                          % this allows to if there is more than one level to continue
                    Idx = find(opt.GroupCount == max(opt.GroupCount),1);    % this assigns the labels of the feedbacktype with the most observations to the complete level 
                    lvl(r+1,2) = table(opt.feedbackType(Idx,:));            % this insert the value rescued from the previous step.
                else
                lvl(r+1,2) = table(opt.feedbackType);                       % this directly assign the only stimulus possible for the level
                end
            end
            c = [table(ones(max(b.levelCounter)+1,1)*j,'VariableNames',...
                {'set'}) lvl];                                              % this codes adds a first column with the set number
            all_lvl = [all_lvl; c];
        end

        % Getting level with problems and saving them in a file 

        for j= min(a.set):max(a.set)
            b = a(a.set==j,:); 
            sset = all_lvl(all_lvl.set==j,:);
            d = groupcounts(sset,'stimulus');
            if diff(d.GroupCount) ~= 0
                fileID = fopen(['C:' filesep 'Users' filesep 'dupre' filesep...
                'count_condition.txt'],'a');
                fprintf(fileID,...
                    "Überprugungs tabbelle \n Different number of cases detected in set %d \n",j); %this shares a message that detected different levels 
                fclose(fileID);
                for r = min(b.levelCounter):max(a.levelCounter)
                    opt = b(b.levelCounter == r,:);
                    if height(opt)>1 & abs(diff(opt.GroupCount)) < 400
                        fileID = fopen(['C:' filesep 'Users' filesep 'dupre' filesep...
                            'count_condition.txt'],'a');
                        fprintf(fileID,...
                            "Problem for %s in level %d \n Difference under 400\n",ptcp,r) ;
                        fclose(fileID);
                    elseif height(opt)>1 && sum(opt.GroupCount) > ...
                            max(b.GroupCount)-0.1*max(b.GroupCount)
                        fileID = fopen(['C:' filesep 'Users' filesep 'dupre' filesep...
                            'count_condition.txt'],'a');
                        fprintf(fileID,...
                            "Problem for %s in level %d \nSum over %d\n",...
                            ptcp,r,max(a.GroupCount)-0.1*max(b.GroupCount));
                        fclose(fileID);
                    end
                end
            else
                %fprintf("Alles gut \n Gleich Anzahl von Fällen an einstellen %d \n ",j);
            end
        end
       
        % Clear all and close
        clear d  b c Idx j sset r a opt fileID
    % add here correction to the problems found. 

    % Building response time
    % FINDING start (finding when the ball is placed in the hand). 
    % into either the left or right hand. Looking for behavioral data ball
    % position
    A = zeros(height(all)-1,1);
    for r = 1:height(all)-1                                                 % going through all observationthorugh one level
        A(r,1) = all.redBallPosition(r+1)~=all.redBallPosition(r);          % through one i the ball changes position. 
    end                                                                     % apparently because of the formulation I'm mmissing some part of level 35 change on red ball position. 
    indx = find(A(:,1)==1);                                                 % getting row number for changes in ball position
    ver = [array2table(indx) all(indx,'levelCounter') all(indx,'set')];     % merging row_start level_counter and set
    start_t = array2table(zeros(max(all.levelCounter),3));                  % preallocating space
    START1 = [];                                                            % building empty matrix
    for k = min(all.set):max(all.set)                                         
        ver2=ver(ver.set==k,:);
        for j = min(ver2.levelCounter):max(ver2.levelCounter)
            F = ver2(ver2.levelCounter==j,'indx');                          % for every level consider the changes ball position only
            start_t(j+1,:) = [F(1,1) array2table(k) array2table(j)];        % for every level save the first change in ball position.
        end
        START1 = [START1 ;start_t];                                         % thi part puts all the starts for every set and level into one long table.
    end
    clear A r indx ver j k F ver2 start_t 
    

    % Finding END
    % This is the ending we finally opted for because when the board explotes
    % is for sure when the trial ends and is not poluted by the push black
    % button cases niether the if the ball felt from the board. The cases that
    % participant drop the ball over the table and made into the board under 6
    % seconds are not excluded. 
    A = zeros(height(all)-1,1);
    for r = 1:height(all)-1                                                 % going through all observationthorugh one level
        A(r,1) = all.levelCounter(r+1)~=all.levelCounter(r);                % through one i the level changes
        % this conincides with  
        A(r,2) = all.set(r);                                                % this adds the matrix the set value 
        A(r,3) = all.levelCounter(r);                                       % this adds to the matrix the level counter value
    end
    indx = find(A(:,1)==1);
    END2 = array2table([indx A(indx,:); 0 0 0 0], 'VariableNames',{'id' 'TorF' 'set' 'lvl'});
    clear A indx r 

    % Creating one table with starts and stops and feedbacktype and correct answers. 
    bhv = [START1(:,2:3) END2(:,1) START1(:,1)];                            % this adds columns of start and end
    bhv.diff = bhv{:,3} - bhv{:,4};                                         % this creates a diff column between start and end
    bhv.diff = bhv.diff/133;                                                % this getting diff column into seconds
    bhv.Properties.VariableNames = {'set' 'lvl' 'end' 'start' 'diff'};      % this gives names to columns
    bhv.stimulus = all_lvl.stimulus;                                        % this adds a column with feedBackType
    
    bhv(bhv.diff <= 0 | bhv.diff > 6 ,:)=[];                                % removing outliers 
    B= bhv;                                                                 % creating instrumental varaible
    r_time.data = B;
    all2(i).rtime = r_time;
    clear pd M h p ci stats bhv all_lvl END2 START1


    %%% ============== Adding mistakes =========================================
    mistakes=[];                                                            % this creates intrumental matrix
    mistakesf=[];                                                           % this creates goal matrix
                                                                            
    data = all2(i).data;                                                    % this extracts the data for the particulart partcp
    A = zeros(size(data,1)-1,4);                                            % this preallocates space for all data
    for line=1:size(data,1)-1                                               % this indicates to go over every row
        A(line,3) = data.correctCounter(line+1)~=data.correctCounter(line); % this looks for diferences in correct counter
        A(line,1) = data.set(line);                                         % this adds to A the set number 
        A(line,2) = data.levelCounter(line);                                % this ads the level counter
        A(line,4) = data.feedbackType(line);                                %this adds the feedback the the moment
    end
    indx = find(A(:,3)==1);                                                 % this gets the exact moment where the correct changed 
    A = A(indx,:);
    mistakes = [A(diff(A(:,2))>1,:) i*ones(size(A(diff(A(:,2))>1,:),1),1) ];
    mistakesf = [mistakesf; mistakes];
   
    clear data A 

    mistakesf(:,2) = mistakesf(:,2)+1;                                      % this goes back to the exact level nummber where the mistake was done.
    mistakes_ag = array2table(mistakesf, 'VariableNames',{'set',...
        'level','mistake','stimuli','participant'});                        % this adds names 
    
    clear line mistakes mistakesf indx
    

    
    %for m=1:size(all2,2)
        behavioral_a =[];
        responsetime = all2(i).rtime.data;
        responsetime.ptcp = ones(size(all2(i).rtime.data,1),1)*i;
        behavioral_a = [behavioral_a;responsetime ];
    %end
    
    for l=1:size(mistakes_ag,1)                                            % It uses variable mistakes_ag to add a variable that has a value one when 
        behavioral_a.accuracy(behavioral_a.ptcp == ...                      % the ball is placed in the wrong hold.
        mistakes_ag.participant(l)&...
        behavioral_a.set == mistakes_ag.set(l)&...
        behavioral_a.lvl == mistakes_ag.level(l),:)=1;
    end
    behavioral_b = [behavioral_b; behavioral_a ];
    clear responsetime l behavioral_a

    

    %%% Adding Heart Rate Data 
    %fs=133;                                                                     % Define the frequency Hz (obs per minute)
    %gr=false;                                                                       
    



end
              
writetable(behavioral_b,[allFolder filesep 'responsetime.csv'])
% Getting rid of all instrumental variables.
clear all parti ptcp i handrot numberOfFolders subdirs r_time B ans behavioral_b
toc



