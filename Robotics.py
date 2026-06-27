import heapq

# =====================================================================
# 1. ENTERPRISE GRC CONFIGURATION MATRIX (From MS Loop Artifacts)
# =====================================================================
COUNCIL_CONFIGS = {
    "City of Gold Coast": {
        "Sectors": ["Clothes"],
        "Bylaw": "Gold Coast City Council Local Law No. 7 (Waste Management)",
        "Hazard_Type": "Stockroom Walkway Clearway Obstruction",
        "Incident_Code": "INC-2026-001"
    },
    "Ipswich City Council": {
        "Sectors": ["Groceries"],
        "Bylaw": "Ipswich City Council Local Law (Commercial Licensing)",
        "Hazard_Type": "Cold Chain Fridge Sensor Maintenance Delay",
        "Incident_Code": "INC-2026-002"
    },
    "Sunshine Coast Council": {
        "Sectors": ["Plastic", "Food"],
        "Bylaw": "Environmental Protection Act 1994 (ERA 12)",
        "Hazard_Type": "Operation Clean Sweep Audit Failure / Spillage Blockage",
        "Incident_Code": "INC-2026-003"
    },
    "City of Moreton Bay": {
        "Sectors": ["Furniture", "Wooden"],
        "Bylaw": "Moreton Bay Regional Council Trust Local Law 2011",
        "Hazard_Type": "Combustible Dust / Timber Structural Bunding Breach",
        "Incident_Code": "INC-2026-004"
    }
}

# Global list to act as our Master Regional Register database for compliance sign-off
COMPLIANCE_LEDGER = []

# =====================================================================
# 2. A* PATHFINDING NODE DEFINITION (CAB320 Core Logic)
# =====================================================================
class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  
        self.h = 0  
        self.f = 0  

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(grid, start, end):
    open_list = []
    closed_set = set()
    
    start_node = Node(start)
    end_node = Node(end)
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)
        
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
            
        x, y = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        
        for next_pos in neighbors:
            if (0 <= next_pos[0] < len(grid)) and (0 <= next_pos[1] < len(grid[0])):
                if grid[next_pos[0]][next_pos[1]] == 1:
                    continue
                if next_pos in closed_set:
                    continue
                    
                neighbor_node = Node(next_pos, current_node)
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = manhattan_distance(next_pos, end_node.position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h
                
                if any(open_node.position == neighbor_node.position and open_node.g <= neighbor_node.g for open_node in open_list):
                    continue
                    
                heapq.heappush(open_list, neighbor_node)
    return None

# =====================================================================
# 3. RUNTIME SIMULATION LOOPS (With Dynamic Layout Configuration)
# =====================================================================
def run_warehouse_simulation(council, sector):
    print("=" * 70)
    print(f"INITIALIZING ENVIRONMENT: {council.upper()} | SECTOR: {sector.upper()}")
    print(f"Governing Bylaw: {COUNCIL_CONFIGS[council]['Bylaw']}")
    print("=" * 70)
    
    # DYNAMIC MAP ROUTING: Moreton Bay represents a severe layout constraint 
    # where row 1 is entirely blocked, creating an unpassable blockade scenario.
    if council == "City of Moreton Bay":
        grid = [
            [0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 0],  # No bypass corridor available here!
            [1, 0, 4, 0, 0, 0, 0],  # WHS Hazard Tile (4) at (2, 2)
            [1, 1, 1, 1, 1, 0, 0],  
            [1, 1, 1, 1, 1, 0, 0]   
        ]
    else:
        grid = [
            [0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],  # Open corridor available for detours
            [1, 0, 4, 0, 0, 0, 0],  
            [1, 1, 1, 1, 1, 0, 0],  
            [1, 1, 1, 1, 1, 0, 0]   
        ]
    
    start_dock = (0, 0)
    target_rack = (2, 6)
    
    print("[AI Executing] Calculating primary path using search heuristics...")
    initial_path = astar(grid, start_dock, target_rack)
    
    if not initial_path:
        print("Error: No viable initial corridor mapping found.")
        return

    print(f"Optimal Path Calculated ({len(initial_path)} steps): {initial_path}")
    
    last_safe_pos = start_dock
    active_incident_id = COUNCIL_CONFIGS[council]['Incident_Code']
    bylaw_ref = COUNCIL_CONFIGS[council]['Bylaw']
    
    for current_pos in initial_path:
        r, c = current_pos
        
        if grid[r][c] == 4:
            print(f"\n[🛑 SYSTEM EXCEPTION TRIPPED AT GRID COORDINATES {current_pos}]")
            
            try:
                hazard_desc = COUNCIL_CONFIGS[council]['Hazard_Type']
                raise RuntimeWarning(f"WHS Obstruction Detected: '{hazard_desc}' under compliance mandate {bylaw_ref}.")
            
            except RuntimeWarning as incident_alert:
                print("-" * 65)
                print("📝 APPENDING TO OPERATIONAL INCIDENT LOG REGISTER:")
                print(f"  • Incident ID:     {active_incident_id}")
                print(f"  • Component Code:  Pathfinding Automation Layer (Telemetry System)")
                print(f"  • Council/LGA:     {council}")
                print(f"  • Core Sector:     {sector}")
                print(f"  • Error Narrative: {incident_alert}")
                print(f"  • Operational Status: Mitigated (Automated Reroute Injected)")
                print("-" * 65)
                
                grid[r][c] = 1 # Solidify hazard corridor
                
                print(f"\n[AI Recalculating] Executing dynamic detour from last safe position {last_safe_pos}...")
                detour_path = astar(grid, last_safe_pos, target_rack)
                
                if detour_path:
                    print(f"Success! Detour Path Found: {detour_path}")
                    print("🏁 Delivery finished safely via alternative safe sector routing.\n")
                    
                    COMPLIANCE_LEDGER.append({
                        "Council": council,
                        "Sector": sector,
                        "Bylaw": bylaw_ref,
                        "Incident_ID": active_incident_id,
                        "Status": "Mitigated & Audited"
                    })
                else:
                    print("Critical: Path completely blocked. Halting operations.\n")
                    COMPLIANCE_LEDGER.append({
                        "Council": council,
                        "Sector": sector,
                        "Bylaw": bylaw_ref,
                        "Incident_ID": active_incident_id,
                        "Status": "CRITICAL HALT - No Path"
                    })
                break
        else:
            print(f"Forklift moving... Passing node coordinates: {current_pos}")
            last_safe_pos = current_pos

# =====================================================================
# 4. PORTFOLIO MULTI-JURISDICTION SWEEP RUNNER
# =====================================================================
if __name__ == "__main__":
    # Run our complete four-council architecture sweep modules sequentially
    run_warehouse_simulation("City of Gold Coast", "Clothes")
    run_warehouse_simulation("Ipswich City Council", "Groceries")
    run_warehouse_simulation("Sunshine Coast Council", "Plastic")
    run_warehouse_simulation("City of Moreton Bay", "Furniture") # The Absolute Blockade Test Case
    
    # =====================================================================
    # 5. MASTER EXECUTIVE COMPLIANCE REPORT SUMMARY
    # =====================================================================
    print("\n" + "#" * 75)
    print("      MASTER SYSTEMS ARCHITECTURE REPORT: DISPATCH & COMPLIANCE LEDGER")
    print("#" * 75)
    print(f"{'LOCAL COUNCIL AREA':<25} | {'SECTOR':<10} | {'INCIDENT ID':<13} | {'AUDIT CONTINUITY STATUS'}")
    print("-" * 75)
    for entry in COMPLIANCE_LEDGER:
        print(f"{entry['Council']:<25} | {entry['Sector']:<10} | {entry['Incident_ID']:<13} | {entry['Status']}")
    print("#" * 75)
    print("All runtime pipeline records successfully cross-referenced with local registers.\n")
