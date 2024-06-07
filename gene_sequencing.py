import tkinter as tk #Import the tkinter module and rename it as 'tk'. This is a Graphical User Interface which allows us to display more user friendly results
from tkinter import filedialog, messagebox #From the tkinter module, import the filedialog (allows user file selection) and messagebox submodules (displays clear messages to the user)

cDNA2amino = {                                       #Create a dictionary called 'cDNA2amino' for translating codons to amino acids
        'TTT':'F', 'TTC':'F', 'TTA':'L', 'TTG':'L',
        'CTT':'L', 'CTC':'L', 'CTA':'L', 'CTG':'L',
        'ATT':'I', 'ATC':'I', 'ATA':'I', 'ATG':'M',
        'GTT':'V', 'GTC':'V', 'GTA':'V', 'GTG':'V',
        'TCT':'S', 'TCC':'S', 'TCA':'S', 'TCG':'S',
        'CCT':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P',
        'ACT':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T',
        'GCT':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A',
        'TAT':'Y', 'TAC':'Y', 'TAA':'*', 'TAG':'*',
        'CAT':'H', 'CAC':'H', 'CAA':'Q', 'CAG':'Q',
        'AAT':'N', 'AAC':'N', 'AAA':'K', 'AAG':'K',
        'GAT':'D', 'GAC':'D', 'GAA':'E', 'GAG':'E',
        'TGT':'C', 'TGC':'C', 'TGA':'*', 'TGG':'W',
        'CGT':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R',
        'AGT':'S', 'AGC':'S', 'AGA':'R', 'AGG':'R',
        'GGT':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G'
}

def translate_cDNA(cDNA_sequence): #Defines a function called 'translate_cDNA()' which translates viable codons into the amino acids from the 'cDNA2amino' dictionary
    protein = '' #Intitalises an empty string to store the protein sequence

    for i in range(0, len(cDNA_sequence), 3): #Iterates over the entire length of the target cDNA sequence, in increments of 3 (no. of bp of a codon), and translates them into corresponding amino acids from the cDNA2amino dictionary 
        codon = cDNA_sequence[i:i+3] #Extracts 3 base pair segments (codons)
        if codon in cDNA2amino: #Checks if these are in the dictionary
            protein += cDNA2amino[codon] #Appends the newly translated codon onto the 'protein' string
        else:
            print(f'Skipping invalid codon:{codon}') #Conditional execution which skips anything that isn't DNA
    return protein #Returns the final protein sequence

def count_walkers(aa_sequence): #Defines a function called 'count_walkers()' which counts the number of walker motifs (GXXXXGKT/S) within a translated protein sequence
    count = 0 #Initialises a walker motif counter
    for i in range(len(aa_sequence)-7): #Iterates over the entire length of the amino acid sequence (-7 to ensure the sequence is at least 8 characters)
        motif = aa_sequence[i:i+8] #Extracts 8 amino acids and stores them in 'motif'
        if motif[0] == 'G' and motif[5] == 'G' and motif[6] == 'K' and motif[7] in 'TS': #If 'motif' contains amino acids in 'GXXXXGKT/S' this order, add 1 to the counter
            count += 1
    return count #Returns the final walker motif count

def process_file(): 
    file_path = filedialog.askopenfilename(filetypes=[('FASTA files', '*.fasta')]) #Opens a 'file dialogue' window which allows the user to choose a .fasta file from their system. Stores the file path in 'file_path'
    if not file_path: #Checks that file_path is not blank
        messagebox.showinfo('Error', 'No file selected. Please select a file.') #Displays error message if 'file_path' is left blank, prompting the user to pick a file
        return

    try:
        with open(file_path, 'r') as fname: #Opens the fasta file and stores it as 'fname'
            target_sequences = fname.read().strip().split('>')  # Split sequences by '>' as all sequence headers start with '>'

        proteins_with_walkers = 0 #Intialises an empty counter for counting proteins containing walker motifs
        result_text = "" #Intialises an empty string for storing result text

        # Translate each sequence
        for sequence in target_sequences: #Iterates over each of the 770 cDNA sequences from the .fasta file
            lines = sequence.strip().split('\n') #Strips each line of any leading and trailing whitespace, splits them into lines and stores them in lines
            header = lines[0] #Stores the first line of 'lines' (the header) in the 'header' variable
            cDNA = ''.join(lines[1:]).replace(' ', '').replace('\n', '') #All the lines in 'sequence' are joined together to create a single string representing the cDNA sequence. Any spaces or newlines are removed
            
            if not cDNA: #If cDNA sequence is empty - skips
                continue
            
            if set(cDNA.upper()) <= {'A', 'T', 'G', 'C'}: #Converts cDNA to uppercase and if cDNA sequence is not composed of solely ATG and/or C, it is disregarded to avoid errors
                protein = translate_cDNA(cDNA) #Uses 'translate_cDNA()' formula to translate sequences stored in cDNA. Stores results in 'protein'
                walker_count = count_walkers(protein) #Uses 'count_walkers()' formula to count the number of walker motifs in the translated protein sequence ('protein' variable)
                #Each of these adds the translation results, along with their labels and headers, to 'result_text' which is displayed by tkinter later
                result_text += f'Header: {header}\n\n' #Adds the corresponding header before resulting protein sequence
                result_text += f'Protein: {protein}\n\n' #Labels each protein sequence
                result_text += f'Number of Walker motifs: {walker_count}\n\n' #Labels the number of walker motifs per protein sequence 

                if walker_count > 0: #This conditional execution adds a count for overall walker motifs for every protein which contains 1 or more walker motifs
                    proteins_with_walkers += 1

            else:
                result_text += f'Skipping invalid cDNA sequence in {header}\n\n' #Produces this message when invalid cDNA sequences are skipped

        result_text += f'Total number of proteins with one or more Walker motifs: {proteins_with_walkers}' #Adds label when all proteins with walker motifs have been tallied.
        
        result_window = tk.Toplevel(core) #Creates a new 'Toplevel' GUI window with tkinter to display the results
        result_window.title('cDNA Translation Results') #Gives this window a title
        
        result_text_widget = tk.Text(result_window, wrap='word') #'tk.Text' function creates a text widget to display the results and fit them within the window 
        result_text_widget.insert(tk.END, result_text) #Inserts 'result_text' into 'result_text_widget'
        result_text_widget.pack(side='left', fill='both', expand=True) #Pakcs 'result_text_widget' into the display window, alligned on the left side (side='left'), filling the space both vertically and horizontally (fill='both'), and expanding to fill any leftover space ('expand=TRUE')

        # Highlight the text 'Total number of proteins with one or more Walker motifs' in yellow
        result_text_widget.tag_add('highlight', 'end-61c', 'end-0c') #Add a tag "highlight" to the range of the 'Total number of proteins with one or more Walker motifs' text
        result_text_widget.tag_config('highlight', background='yellow', foreground='black') #Configure the 'highlight' tag with desired background and foreground colors

        scroll_vertical = tk.Scrollbar(result_window, orient='vertical', command=result_text_widget.yview) #Function creates a vertical ('orient='vertical'') scroll bar in the result_window to view all the results easily. 
        scroll_vertical.pack(side='right', fill='y') #Fits the scrollbar to fill the right-hand y-axis
        result_text_widget.config(yscrollcommand=scroll_vertical.set) #'yscrollcommand' attribute of the text is configured to scroll with the scrollbar

        close_button = tk.Button(result_window, text='Close', command=result_window.destroy) #Function creates a button in the window which allows the user to exit the window
        close_button.pack() #Adds it to the result window

    except Exception as err: #Catches any errors which occur during the opening of the file or processing of results
        messagebox.showerror('Error', f'An error occurred: {err}') #Displays the error message in a message box so the user knows the problem

core = tk.Tk() #Creates the main 'tkinter' window to display all other GUI elements
core.title('DNA Translation Tool') #Titles the window 'DNA Translation Tool'

process_button = tk.Button(core, text='Select File', command=process_file) #Creates a button which allows the user to select a file from their computer to be processed
process_button.pack(pady=10) #Packed into main window with some padding

core.mainloop() #Starts the tkinter event loop, which detects user interactions and continues running until the 'core' window is closed

#ChatGPT3.5: https://chat.openai.com/ assisted with the creation of this programme.