import random
import csv
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox as tkMessageBox
import time
from tkinter import simpledialog 


#Class defining the parameters of the player
class Player:
    def __init__(self, name,RestrictArea_FGpercent,Paint_FGpercent,MidRange_FGpercent,LeftCorner3_FGpercent,RightCorner3_FGpercent,AboveBreak3_FGpercent,\
                 RestrictArea_FGA,Paint_FGA,MidRange_FGA,LeftCorner3_FGA,RightCorner3_FGA,Totals_FGA,AboveBreak3_FGA,\
                 RestrictArea_FGM,Paint_FGM,MidRange_FGM,LeftCorner3_FGM,RightCorner3_FGM,AboveBreak3_FGM,Totals_FGM): #Player stats, hardcoded right now
        self.name = name.strip()   # Remove any whitespace
        self.RestrictArea_FGpercent = float(RestrictArea_FGpercent)
        self.Paint_FGpercent = float(Paint_FGpercent)
        self.MidRange_FGpercent = float(MidRange_FGpercent)
        self.LeftCorner3_FGpercent = float(LeftCorner3_FGpercent)
        self.RightCorner3_FGpercent = float(RightCorner3_FGpercent)
        self.AboveBreak3_FGpercent = float(AboveBreak3_FGpercent)

        self.RestrictArea_FGA = float(RestrictArea_FGA)
        self.Paint_FGA = float(Paint_FGA)
        self.MidRange_FGA = float(MidRange_FGA)
        self.LeftCorner3_FGA = float(LeftCorner3_FGA)
        self.RightCorner3_FGA = float(RightCorner3_FGA)
        self.Totals_FGA = float(Totals_FGA)
        self.AboveBreak3_FGA = float(AboveBreak3_FGA)

        self.RestrictArea_FGM = float(RestrictArea_FGM)
        self.Paint_FGM = float(Paint_FGM)
        self.MidRange_FGM = float(MidRange_FGM)
        self.LeftCorner3_FGM = float(LeftCorner3_FGM)
        self.RightCorner3_FGM = float(RightCorner3_FGM)
        self.AboveBreak3_FGM = float(AboveBreak3_FGM)
        self.Totals_FGM = float(Totals_FGM)  #THESE TOTALS STATS ARE BROKEN but not being used
        self.total2PA=self.RestrictArea_FGA+self.Paint_FGA+self.MidRange_FGA
        self.total3PA=self.LeftCorner3_FGA+self.RightCorner3_FGA+self.AboveBreak3_FGA
        if self.total2PA == 0:
            self.TwoPTpercent=0
        else:
            self.TwoPTpercent = (self.RestrictArea_FGM+self.Paint_FGM+self.MidRange_FGM)/(self.total2PA)
        if self.total3PA == 0:
            self.ThreePTpercent=0
        else:   
            self.ThreePTpercent = (self.LeftCorner3_FGM+self.RightCorner3_FGM+self.AboveBreak3_FGM)/(self.total3PA)

        self.pointsScored = 0
        self.twoPTM = 0
        self.twoPTA = 0
        self.threePTM = 0
        self.threePTA = 0
        self.fga=self.RestrictArea_FGA+self.Paint_FGA+self.MidRange_FGA+self.LeftCorner3_FGA+self.RightCorner3_FGA+self.AboveBreak3_FGA
        self.lotsOfShots2=random.choices([1,0],weights=[self.TwoPTpercent,1-self.TwoPTpercent],k=300)
        self.lotsOfShots3=random.choices([1,0],weights=[self.ThreePTpercent,1-self.ThreePTpercent],k=300)

    def reset_score(self):
        self.pointsScored=0

    def get_score(self):
        return self.pointsScored

    def get_splits(self):
        return(self.twoPTM,self.twoPTA,self.threePTM,self.threePTA)

    def reset_splits(self):
        self.twoPTM = 0
        self.twoPTA = 0
        self.threePTM = 0
        self.threePTA = 0
        
    def shoot2pt(self,turn):
        #lotsOfShots=random.choices([1,0],weights=[self.TwoPTpercent,1-self.TwoPTpercent],k=500)
        if self.lotsOfShots2[turn] == 1: #Selecting one shot out of the lots of shots
            return True  #Make shot
        else:
            return False
    def shoot3pt(self,turn):
        #lotsOfShots=random.choices([1,0],weights=[self.ThreePTpercent,1-self.ThreePTpercent],k=500)
        if self.lotsOfShots3[turn] == 1: #Selecting one shot out of the lots of shots
            return True  #Make shot
        else:
            return False




class Team:
    def __init__(self,name,pct2PA,pct3PA): #team name, %of shots 2pt, %of shots 3pt, possessions per game
        self.name = name
        self.players = []
        self.pct2PA = pct2PA
        self.pct3PA = pct3PA
    def addPlayer(self,player):
        self.players.append(player) #should be a player object
    def reset_scores(self):
        for player in self.players:
            player.reset_score()
    def get_scores(self):
        scores = []
        for player in self.players:
            scores.append(player.get_score())
        return scores
    def get_shooting_splits(self):
        splits = []
        for player in self.players:
            splits.append(player.get_splits())
        return splits
    def reset_splits(self):
        for player in self.players:
            player.reset_splits()

class GUI:
    
    class optionDialog(tk.simpledialog.Dialog):
        def body(self,parent):#self,GUI.window

            tk.Label(parent, text="Team 1 name:").grid(row=0,column=0)
            tk.Label(parent, text="Team 2 name:").grid(row=1,column=0)
            tk.Label(parent, text="Team 1 3 point attempt %:").grid(row=2,column=0) #
            tk.Label(parent, text="Team 2 3 point attempt %:").grid(row=3,column=0) #
            

            self.team1NameEntry = tk.Entry(parent)
            self.team2NameEntry = tk.Entry(parent)
            self.team1PossEntry = tk.Entry(parent) #
            self.team2PossEntry = tk.Entry(parent) #
            
            self.team12PTattemptPercent = tk.Entry(parent)
            self.team22PTattemptPercent = tk.Entry(parent)
            self.team13PTpPercent = tk.Entry(parent)
            self.team23PTpPercent = tk.Entry(parent)      

            self.team1NameEntry.grid(row=0, column=1)
            self.team2NameEntry.grid(row=1, column=1)
            self.team13PTpPercent.grid(row=2, column=1) #
            self.team23PTpPercent.grid(row=3, column=1) #

            #poss = int(self.team1PossEntry.get()) + int(self.team1PossEntry.get())
            return 0 # initial focus

        def apply(self):
            pass
            

        
    def __init__(self,game): #Initializes all the buttons and stuff that is needed. PASS THE game OBJECT
        self.game=game
        
        self.window = tk.Tk()
        self.window.title("The MBA")

        self.menubar = tk.Menu(self.window)
        self.menubar.add_command(label="Options", command=self.set_options)
        self.menubar.add_command(label="Save", command=self.save_game)
        self.menubar.add_command(label="Load", command=self.load_game)
        self.menubar.add_separator()
        self.menubar.add_command(label="Exit", command=self.window.quit)
        self.window.config(menu=self.menubar)

        self.window.columnconfigure(0, weight=1, minsize=75)
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.columnconfigure(1, weight=1, minsize=50)
        self.window.rowconfigure(1, weight=1, minsize=50)
        self.window.rowconfigure(2, weight=1, minsize=20)
        self.window.columnconfigure(1, weight=1, minsize=100)

        self.playerFrame=tk.LabelFrame(
            master = self.window,
            relief=tk.GROOVE,
            borderwidth=2,text="Choose Players",width=300,height=300)
        
        self.playerFrame.grid(row=0, column=0, padx=10, pady=10,sticky="n")


        self.playerSelector = tk.Listbox(self.playerFrame,width=40,height=30,selectmode=tk.SINGLE)
        self.playerSelector.pack(padx=5, pady = 5)

        self.addFrame=tk.Frame(
            master = self.window,
            relief=tk.FLAT,
            borderwidth=2, width=150
        )
        self.addFrame.grid(row=0, column=1, padx=10, pady=10,sticky="ne")
        
        self.team1addButton=tk.Button(self.addFrame, text="ADD",font=font.Font(family='Impact',size=24, weight='bold'),command=self.add_to_team1,bg="blue")
        self.team1addButton.pack(padx=10, pady = 10)

        self.team1delButton=tk.Button(self.addFrame, text="DEL",font=font.Font(family='Impact',size=24, weight='bold'),command=self.del_from_team1,bg="red")
        self.team1delButton.pack(padx=10, pady = 50)

        self.team2addButton=tk.Button(self.addFrame, text="ADD",font=font.Font(family='Impact',size=24, weight='bold'),command=self.add_to_team2,bg="blue")
        self.team2addButton.pack(padx=10, pady = 10)

        self.team2delButton=tk.Button(self.addFrame, text="DEL",font=font.Font(family='Impact',size=24, weight='bold'),command=self.del_from_team2,bg="red")
        self.team2delButton.pack(padx=10, pady = 50)

        self.teamsFrame=tk.LabelFrame(
            master = self.window,
            relief=tk.GROOVE,
            borderwidth=2,text="Teams",width=300,height=400)
        self.teamsFrame.grid(row=0, column=2, padx=10, pady=10,sticky="n")

        #find out team names
        team1name=self.game.team1.name
        team2name=self.game.team2.name

        self.team1frame=tk.LabelFrame(
            master = self.teamsFrame,
            relief=tk.RAISED,
            labelanchor = tk.N,
            borderwidth=2,text=team1name,width=250,height=250)
        self.team1frame.grid(row=0, column=0, padx=10, pady=5)
        
        self.team2frame=tk.LabelFrame(
            master = self.teamsFrame,
            relief=tk.RAISED,
            labelanchor = tk.N,
            borderwidth=2,text=team2name,width=250,height=250)
        self.team2frame.grid(row=1, column=0, padx=10, pady=5)

        self.teamsFrame.grid(row=0, column=2, padx=10, pady=10,sticky="n")
        
        
        self.team1score=tk.Label(master=self.team1frame,text="Score: 0",font=font.Font(family='Impact',size=18))
        self.team1score.grid(row=0,column=0,padx=5,pady=0)

        self.team2score=tk.Label(master=self.team2frame,text="Score: 0",font=font.Font(family='Impact',size=18))
        self.team2score.grid(row=0,column=0,padx=5,pady=0)

        self.team1list = tk.Listbox(self.team1frame,width=40,height=10)
        self.team1list.grid(row=1,column=0,padx=5,pady=7,sticky="s")

        self.team2list = tk.Listbox(self.team2frame,width=40,height=10)
        self.team2list.grid(row=1,column=0,padx=5,pady=7,sticky="s")

        commentframe=tk.Frame(
            master = self.window,
            relief=tk.SUNKEN,
            borderwidth=2, width=250, height=30, bg="white"
        )
        commentframe.grid(row=1, column=0, padx=10, pady=10,sticky="sw")
        commentframe.grid_propagate(0)
        self.commentarybox = tk.Label(master=commentframe, bg="white",text="Select 5 players per Team")
        self.commentarybox.grid(row=0, column=0, padx=5, pady = 5) 

        doneButton=tk.Button(master=self.window,text="TIPOFF!",bg="red",fg="white",command=self.start_game, height=2)
        doneButton.grid(row=1,column=2,sticky="s",padx=10,pady=10)

        


    def start_gui(self):
        self.window.mainloop()

    def set_options(self):
        self.dialogBox = self.optionDialog(self.window)
        

    def save_game(self):
        pass

    def load_game(self):
        pass
        
    def add_players(self,playernames): #playernames is a list
        for player in playernames:
            self.playerSelector.insert(tk.END,player)
        #self.playerSelector.current(309)

    def add_to_team1(self):
        if self.team1list.size() > 4:
            tkMessageBox.showwarning("Error","Only 5 players per team.")
            return
        selectedPlayer=self.playerSelector.curselection()[0]
        selectedPlayerName=self.playerSelector.get(selectedPlayer)
        self.team1list.insert(tk.END,selectedPlayerName)

    def add_to_team2(self):
        if self.team2list.size() > 4:
            tkMessageBox.showwarning("Error","Only 5 players per team.")
            return
        selectedPlayer=self.playerSelector.curselection()[0]
        selectedPlayerName=self.playerSelector.get(selectedPlayer)
        self.team2list.insert(tk.END,selectedPlayerName)

    def del_from_team1(self):
        selectedPlayer=self.team1list.curselection()[0]
        selectedPlayerName=self.team1list.get(selectedPlayer)
        self.team1list.delete(selectedPlayer)
        # delete from Team as well
        playerNameToDelete = selectedPlayerName.split("\t")[0].strip()
        self.game.del_from_team1(playerNameToDelete)
    
    def del_from_team2(self):
        selectedPlayer=self.team2list.curselection()[0]
        selectedPlayerName=self.team2list.get(selectedPlayer)
        self.team2list.delete(selectedPlayer)
        # delete from Team as well
        playerNameToDelete = selectedPlayerName.split("\t")[0].strip()
        self.game.del_from_team1(playerNameToDelete)

    def get_team_lists(self):
        team1players=[]
        team1players=[self.team1list.get(i).split("\t")[0].strip() for i in range(5)]

        team2players=[]
        team2players=[self.team2list.get(i).split("\t")[0].strip() for i in range(5)]
        
        return [team1players,team2players] #Returns lists of lists of strings
            
    def start_game(self):
        self.game.init_game()
        teamLists=self.get_team_lists()
        if len(teamLists[0]) !=5 or len(teamLists[1]) !=5:
           tkMessageBox.showwarning("Error","You need 5 players per team.")
           return
        self.game.add_players_to_teams(teamLists[0],teamLists[1])

        scores = [0,0,"Starting"]
        while scores:
            self.team1score.config(text=f"Score: {scores[0]}")
            self.team2score.config(text=f"Score: {scores[1]}")
            self.commentarybox.config(text=scores[2])
            self.team1score.update()
            self.team2score.update()
            self.commentarybox.update()
            # Get scoring player name 
            scoringplayername = "None"
            idx = scores[2].find("made")
            if idx != -1:
                scoringplayername=scores[2][:idx].strip()

            # Update player scores
            team1playerscores = self.game.get_team1_scores()
            team2playerscores = self.game.get_team2_scores()

            team1splits = self.game.get_team1_splits()
            team2splits = self.game.get_team2_splits()
            

            team1players = [self.team1list.get(i).split('\t')[0].strip() for i in range(5)]
            team2players = [self.team2list.get(i).split('\t')[0].strip() for i in range(5)] 

            self.team1list.delete(0,tk.END)
            for i in range(5):
                self.team1list.insert(tk.END, f"{team1players[i]} \t\t {team1playerscores[i]} \t\t 2PT {team1splits[i][0]}/{team1splits[i][1]} 3PT {team1splits[i][2]}/{team1splits[i][3]}")
                if scoringplayername == team1players[i]:
                    self.team1list.itemconfig(tk.END, fg="red")
            self.team2list.delete(0,tk.END)
            for i in range(5):
                self.team2list.insert(tk.END, f"{team2players[i]} \t\t {team2playerscores[i]} \t\t 2PT {team2splits[i][0]}/{team2splits[i][1]} 3PT {team2splits[i][2]}/{team2splits[i][3]}")
                if scoringplayername == team2players[i]:
                    self.team2list.itemconfig(tk.END, fg="red" )

            if self.game.turnsPlayed%50 == 0 and self.game.turnsPlayed > 0 :
                self.commentarybox.config(text="End of Quarter")
                self.commentarybox.update()
                time.sleep(3)
            time.sleep(0.15)
            scores = self.game.play_turn()
            if not scores:
                self.commentarybox.config(text="End of Game")
                
                self.commentarybox.update()


    
    
#game logic
class Game:
    def __init__(self,teams,players,numPossessions): #players is the list of ALL PLAYER OBJECTS. TBD Should go in League class later
        self.team1=teams[0]
        self.team2=teams[1]
        self.teams=teams
        
        self.team1Score=0
        self.team2Score=0

        self.players=players
        self.numPossessions=numPossessions
        self.turnsPlayed=0

        self.fgaOrder=[]

    def add_players_to_teams(self,team1players,team2players):

        for playerName in team1players:
            for playerObj in self.players:
                if playerObj.name == playerName:
                    self.team1.addPlayer(playerObj)
                    break

        for playerName in team2players:
            for playerObj in self.players:
                if playerObj.name == playerName:
                    self.team2.addPlayer(playerObj)
                    break

        #Once teams are know figure out distribution of possessions for players
        playerFGAs={} # <name> : <fga>
        allAttempts=[]
        
        allPlayerNames=team1players+team2players
        totalFGA=0 #FOR BOTH TEAMS
        for playerName in allPlayerNames:
            for player in self.team1.players:
                if player.name == playerName:
                    playerFGAs[player.name] = player.fga
                    totalFGA+=player.fga

            for player in self.team2.players:
                if player.name == playerName:
                    playerFGAs[player.name] = player.fga
                    totalFGA+=player.fga
                    
        normFactor=self.numPossessions/totalFGA

        for playerName in allPlayerNames:
            normFGA=int(round(normFactor*playerFGAs[playerName]))
            playerFGAs[playerName]=normFGA #filling out the dict: Now it is normalized

        for playerName in allPlayerNames:
            for attemptNumber in range(1,playerFGAs[playerName]):
                allAttempts.append(playerName) 

        self.fgaOrder=random.sample(allAttempts,len(allAttempts))

        # if numPossession is more than length of fgaOrder,  add at the end
        for i in range(1 + self.numPossessions - len(self.fgaOrder)):
               randomPlayerName = random.choice(allPlayerNames)
               self.fgaOrder.append(randomPlayerName)
                
    def init_game(self):
        self.team1Score=0
        self.team2Score=0
        self.turnsPlayed=0
        self.team1.reset_scores()
        self.team2.reset_scores()
        self.team1.reset_splits()
        self.team2.reset_splits()
        self.team1.players = []
        self.team2.players = []


    def play_turn(self):
        if self.turnsPlayed >= self.numPossessions:
            return False #ERROR

        playerNameWithBall = self.fgaOrder[self.turnsPlayed]
        for player in self.team1.players + self.team2.players:
            if player.name == playerNameWithBall:
                playerWithBall = player
                break


        turnoutcome = f"{playerWithBall.name} did not score"

        position=random.choice(("3","2")) #Goes to 3pt line or 2pt
        
        if position == "3":  #if they are going to shoot a 3
            make=playerWithBall.shoot3pt(self.turnsPlayed)
            if make == True: #true is make
                #print(f"{playerWithBall.name} made a 3")
                turnoutcome = f"{playerWithBall.name} made a 3"
                if playerWithBall in self.team1.players: 
                    self.team1Score +=3
                    playerWithBall.pointsScored+=3
                    playerWithBall.threePTM += 1
                    playerWithBall.threePTA += 1
                    playerWithBall=random.choice(self.team2.players) #Inbound ball to person on other team
                elif playerWithBall in self.team2.players:
                    self.team2Score +=3
                    playerWithBall.pointsScored+=3
                    playerWithBall.threePTM += 1
                    playerWithBall.threePTA += 1
                    playerWithBall=random.choice(self.team1.players)
                else:
                    #print("Apparently the ball went to the ref or something.")
                    pass
            elif make == False:  #That's a brick
                playerWithBall.threePTA += 1
                playerWithBall=random.choice(self.team1.players+self.team2.players)
                
                    
        if position == "2":  #if they are going to shoot a 3
            make=playerWithBall.shoot2pt(self.turnsPlayed)
            if make == True: #true is make
                #print(f"{playerWithBall.name} made a 2")
                turnoutcome = f"{playerWithBall.name} made a 2"
                if playerWithBall in self.team1.players: 
                    self.team1Score +=2
                    playerWithBall.pointsScored+=2
                    playerWithBall.twoPTM += 1
                    playerWithBall.twoPTA += 1
                    playerWithBall=random.choice(self.team2.players)
                elif playerWithBall in self.team2.players:
                    self.team2Score +=2
                    playerWithBall.pointsScored+=2
                    playerWithBall.twoPTM += 1
                    playerWithBall.twoPTA += 1
                    playerWithBall=random.choice(self.team1.players)
                else:
                    #print("Apparently the ball went to the ref or something.")
                    pass
            elif make == False:
                playerWithBall.twoPTA += 1
                playerWithBall=random.choice(self.team1.players+self.team2.players)

        self.turnsPlayed+=1 
        """
        print(f"Possession #{self.turnsPlayed}")          
        
        print(f"The {self.team1.name} individual player scores")
        for player in self.team1.players:
            print(f"{player.name} scored {player.pointsScored} points")
        
        print("")

        print(f"The {self.team2.name} individual player scores")
        for player in self.team2.players:
            print(f"{player.name} scored {player.pointsScored} points")
        """

        #print(self.team1Score,self.team2Score,turnoutcome)
        return [self.team1Score,self.team2Score,turnoutcome]

    def get_team1_scores(self):
        return self.team1.get_scores()

    def get_team2_scores(self):
        return self.team2.get_scores()

    def get_team1_splits(self):
        return self.team1.get_shooting_splits()

    def get_team2_splits(self):
        return self.team2.get_shooting_splits()

    def del_from_team1(self,playerName):
        idx= 0
        for player in self.team1.players:
            if player.name == playerName:
               print("In Team 1 Delete for player " + playerName)
               del self.team1.players[idx]
               break
            idx+=1

    def del_from_team2(self,playerName):
        idx= 0
        for player in self.team2.players:
            if player.name == playerName:
                print("In Team2 Delete for player " + playerName)
                del self.team2.players[idx]
                break
            idx+=1




def main():
    
    #Getting REAL data
    players=[]#list of the objects of every NBA player
    playernames=[] #list of all player names FOR GUI

    with open("players.csv") as rawData:
        csv_reader=csv.DictReader(rawData,delimiter = ",")
        line_count=0
        for row in csv_reader:
            #print(row["Name"])
            if "-" in row.values():
                continue
            playernames.append(row["Name"].strip())
            p=Player(row["Name"],row["RestrictArea_FGpercent"],row["Paint_FGpercent"],row["MidRange_FGpercent"],
                     row["LeftCorner3_FGpercent"],row["RightCorner3_FGpercent"],row["AboveBreak3_FGpercent"],
                     row["RestrictArea_FGA"],row["Paint_FGA"],row["MidRange_FGA"],row["LeftCorner3_FGA"], 
                     row["RightCorner3_FGA"],row["Totals_FGA"],row["AboveBreak3_FGA"],row["RestrictArea_FGM"],
                     row["Paint_FGM"],row["MidRange_FGM"],row["LeftCorner3_FGM"],row["RightCorner3_FGM"],
                     row["AboveBreak3_FGM"],row["Totals_FGM"])
            #print(p.ThreePTpercent)
            players.append(p)


    """        
    #Assigning teams and team data
    team1name=input("Team 1 name: ")
    team1_2pct2PA=float(input("Team 1 tendency to shoot 2pt: "))
    team1_2pct3PA=float(input("Team 1 tendency to shoot 3pt: "))
    #team1poss=int(input("Team 1 possessions per game: "))

    team2name=input("Team 2 name: ")
    team2_2pct2PA=float(input("Team 2 tendency to shoot 2pt: "))
    team2_2pct3PA=float(input("Team 2 tendency to shoot 3pt: "))
    poss=int(input("Total possessions per game: "))

    team1=Team(team1name,team1_2pct2PA,team1_2pct3PA)
    team2=Team(team2name,team2_2pct2PA,team2_2pct3PA) 
    """

    #Hardcode teams and team data
    team1name="The Easy Breezies"
    team1_2pct2PA=0.5
    team1_2pct3PA=0.5

    team2name="The Jolly Follies"
    team2_2pct2PA=0.5
    team2_2pct3PA=0.5
    
    poss= 200

    team1=Team(team1name,team1_2pct2PA,team1_2pct3PA)
    team2=Team(team2name,team2_2pct2PA,team2_2pct3PA) 
    
    teams=[team1,team2]

    #poss = team1poss + team2poss

    game=Game(teams,players,poss) #initialize a game

    #GUI
    gui=GUI(game)

    gui.add_players(playernames)
    gui.start_gui()# gui starts in end because it takes over 
    



if __name__ == "__main__":
    main()

          

