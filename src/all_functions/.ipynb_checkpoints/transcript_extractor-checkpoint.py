def preprocessing(transcript_lines):
    new_transcript_lines=[]
    for LL in transcript_lines:
        LL1=LL
        while True:
            LL0=LL1
            if LL0.startswith('(') and ':' in LL0 and ')' in LL0:
                if LL0.startswith('(') and LL0.index(':')>LL0.index(')'):
                    begin=LL0[:LL0.index(')')+1]
                    end=LL0[LL0.index(')')+1:]

                    LL1=(end+begin).strip()
                else:
                    LL1=LL0
                    break
            else:
                LL1=LL0
                break
        new_transcript_lines.append(LL0.strip())
    return new_transcript_lines
    

def extraction(transcript_lines):
    dialogue=[]
    scene=[]
    title=[]
    writer_story=[]
    transcriber=[]
    notes=[]
    k=0
    scene_loc='unknown'
    new_scene_loc=False

    while True:
        if new_scene_loc:
            scene_loc=new_scene_loc
            new_scene_loc=False
        
        try:
            LL=transcript_lines[k]
        except:
            print(k)
            break

        if LL.startswith('the one'):
            title.append(LL)
            k+=1
        elif LL.startswith('written by') or LL.startswith('story by') or LL.startswith('story'):
            writer_story.append(LL)
            k+=1
        elif LL.startswith('transcribed by') or LL.startswith('additional transcribing by') or LL.startswith('episodes orginally transcribed by'):
            transcriber.append(LL)
            k+=1           
            
        elif LL.startswith('[') and ':' in LL:
            scene_loc=LL.split(':')[1].split(',')[0].split('.')[0].split(']')[0].strip()
            scene.append(LL)
            k+=1
            
        elif LL.startswith('('):
            notes.append(LL)
            k+=1

        elif '[' in LL and not LL.startswith('[') and ':' in LL:
            if "]" in LL:
                LL_parts=LL.split('[')
                k+=1

            else:
                LL_parts=' '.join([LL,transcript_lines[k+1]]).split('[')
                k+=2

            txt_dialogue="["+scene_loc+"]"+'-'+LL_parts[0]

            try:            
                scene_loc=LL_parts[1].split(':')[1].split(',')[0].strip()
                scene.append(LL_parts[1])

                dialogue.append(txt_dialogue)
            except:
                txt_list=LL_parts[1].split(']')
                if len(txt_list)>1:
                    txt_dialogue+=txt_list[1]
                else:
                    txt_dialogue+=txt_list[0]
                    
                i=0
                while True:
                    LL_add=transcript_lines[k+i]
                    if ':' in LL_add or (LL_add=='end'):
                        dialogue.append(txt_dialogue)
                        break
                    else:
                        txt_dialogue+=' '+LL_add
                        i+=1

                # print('ERROR.',LL_parts[1])
                k+=i

        elif ':' in LL:
            LL0=[]
            LL0.append(LL)
            k+=1

            while True:
                try:
                    LL=transcript_lines[k]
                except:
                    LL='end'
                    
                    
                if ':' in LL and '[' in LL and LL.index(':')>LL.index('['):

                    if "]" in LL:
                        LL_parts=LL.split('[')
                        if len(LL_parts)>2:
                            LL_parts=[i for i in LL_parts if i!='']
                        new_scene_loc=LL_parts[1].split(':')[1].split(',')[0].strip()
                        LL0.append(LL_parts[0])
                        k+=1
                    else:
                        LL_parts=' '.join([LL,transcript_lines[k+1]]).split('[')
                        new_scene_loc=LL_parts[1].split(':')[1].split(',')[0].strip()
                        LL0.append(LL_parts[0])
                        k+=2
                        
                elif ':' in LL or (LL=='end'):
                    txt_dialogue="["+scene_loc+"]"+'-'+' '.join(LL0)
                    dialogue.append(txt_dialogue)
                    break
                else:
                    LL0.append(LL)
                    k+=1
        else:
            notes.append(LL)
            k+=1
            
    id_dialogue=[i for i in range(len(dialogue))]
    dialogue2=[str(i)+'~'+dd for i,dd in zip(id_dialogue,dialogue)]
    notes2=[i for i in notes if i!='']
    extract_dict={'dialogue':dialogue2,
            'scenes':scene,
            'title':title,
            'writers':writer_story,
            'transcriber':transcriber,
            'others':notes2}
    
    return extract_dict    