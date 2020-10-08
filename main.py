from functions import func
import numpy as np
import math
import matplotlib.pyplot as plt

constraint = np.loadtxt("input.txt",delimiter =",",encoding='utf-8')

def brute_force(constraint):
    min_x = new_x = constraint[0][0]
    max_x = constraint[0][1]
    min_y = new_y = constraint[1][0]
    max_y = constraint[1][1]

    for i in range(int(min_x),int(max_x),1):
        for j in range(int(min_y),int(max_y),1):
            if func(i,j) < func(new_x,new_y):
                new_x = i
                new_y = j
                #print("現在的最小值是: x= ", new_x ,' y= ', new_y ,' z= ', func(new_x,new_y))
                
    print("brute_force_result: \n x:",new_x,'\n y:',new_y,'\n',func(new_x,new_y))

def sa(constraint):
    T = 1000 #initiate temperature
    Tmin = 10 #minimum value of terperature
    x = np.random.uniform(low=constraint[0][0],high=constraint[0][1]) #initiate x
    y = np.random.uniform(low=constraint[1][0],high=constraint[1][1]) #initiate y
    best_x, best_y = (float('inf'), ) * 2 #record optimized x y
    k = 50 #times of internal circulation 
    z , new_z , min_z= (float('inf'), ) * 3 #initiate result
    t = 0 #time
    K = 0.001 #coefficiency of T
    prev_z = z #record previous z

    z_best_counter = 0 # counter for detecting how stable the cost_best currently is

    while T >= Tmin and z_best_counter < 50:
        for i in range(k):
            #calculate y
            z = func(x,y)
            #print("round",i," z: ",z)
            #generate a new x in the neighboorhood of x by transform function
            new_x = x + np.random.uniform(low=-0.055,high=0.055)*T
            new_y = y + np.random.uniform(low=-0.055,high=0.055)*T
            if ( constraint[0][0] < new_x and new_x <= constraint[0][1]
                and constraint[1][0] < new_y and new_y <= constraint[1][1] ):
                new_z = func(new_x , new_y)

                # p = np.exp(-(new_y - z)/(K*T))
                # r = np.random.rand()
                #print("new_y-z=",new_y - z,"r:",r,"p:",p)

                #print("round",i," new_y:",new_y)
                if new_z < z:
                    x = new_x
                    y = new_y
      
                else:
                    #metropolis principle
                    p = np.exp(-(new_z - z)/(K*T))
                    r = np.random.rand()
                    #print("new_z-z=",new_z - z,"r:",r,"p:",p)
                    if r < p:
                        # print("true!")
                        x = new_x
                        y = new_y
                if new_z < min_z:
                    min_z = new_z
                    best_x = x
                    best_y = y                

        t += 1
        print("Time:",t)
        T=1000/(1+t)
        
        if abs(prev_z - min_z) < 1e-12: #close enough to be stable
          z_best_counter += 1
        else:    
          z_best_counter = 0    # Not stable yet, reset

        prev_z = min_z

        print("Temperature:", "%.2f°C" % round(T, 2),
              " Z= ", "%.3f" % round(min_z, 3),
              " Optimization Threshold:", "%d" % z_best_counter)
        
    print ("sa_result: \n x:%.3f"%best_x,'\n',"y:%.3f"%best_y,'\n',"%.3f"%func(best_x,best_y))

#brute_force(constraint)
sa(constraint)
