import java.util.*;

class Truck {
    int width, length, cost;
    boolean[][] occupied;

    Truck(int width, int length, int cost) {
        this.width = width;
        this.length = length;
        this.cost = cost;
        this.occupied = new boolean[width][length];
    }

    boolean canPlaceItem(int w, int l, int x, int y) {
        if (x + w > width || y + l > length) return false;
        for (int i = x; i < x + w; i++) {
            for (int j = y; j < y + l; j++) {
                if (occupied[i][j]) return false;
            }
        }
        return true;
    }

    void placeItem(int w, int l, int x, int y) {
        for (int i = x; i < x + w; i++) {
            for (int j = y; j < y + l; j++) {
                occupied[i][j] = true;
            }
        }
    }

    void removeItem(int w, int l, int x, int y) {
        for (int i = x; i < x + w; i++) {
            for (int j = y; j < y + l; j++) {
                occupied[i][j] = false;
            }
        }
    }
}

class Item {
    int width, length;

    Item(int width, int length) {
        this.width = width;
        this.length = length;
    }
}

class Solution {
    int truckIndex, x, y, rotation;

    Solution(int truckIndex, int x, int y, int rotation) {
        this.truckIndex = truckIndex;
        this.x = x;
        this.y = y;
        this.rotation = rotation;
    }
}

public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int N = scanner.nextInt();
        int K = scanner.nextInt(); 
        
        Item[] items = new Item[N];
        for (int i = 0; i < N; i++) {
            int w = scanner.nextInt();
            int l = scanner.nextInt();
            items[i] = new Item(w, l); 
        }
        
        Truck[] trucks = new Truck[K];
        for (int i = 0; i < K; i++) {
            int W = scanner.nextInt();
            int L = scanner.nextInt();
            int c = scanner.nextInt();
            trucks[i] = new Truck(W, L, c); 
        
        List<Solution> solutions = solve(items, trucks);

        for (int i = 0; i < N; i++) {
            Solution sol = solutions.get(i);
            System.out.println((i + 1) + " " + sol.truckIndex + " " + sol.x + " " + sol.y + " " + sol.rotation);
        }
        
        scanner.close();
    }

    private static List<Solution> solve(Item[] items, Truck[] trucks) {
        List<Solution> solutions = new ArrayList<>();
        Random r = new Random();
        double temperature = initTemperature(); 
        double coolingRate = 0.003; 
        int maxIter = 1000; 
        
        int[] assignment = new int[items.length]; // Mảng lưu trữ chỉ số xe tải chứa từng món hàng
        int[] xCoord = new int[items.length]; 
        int[] yCoord = new int[items.length]; 
        int[] rotation = new int[items.length]; // Mảng lưu trữ trạng thái xoay của từng món hàng
        
        for (int i = 0; i < items.length; i++) {
            boolean placed = false;
            for (int k = 0; k < trucks.length && !placed; k++) {
                for (int x = 0; x < trucks[k].width && !placed; x++) {
                    for (int y = 0; y < trucks[k].length && !placed; y++) {
                        if (trucks[k].canPlaceItem(items[i].width, items[i].length, x, y)) {
                            trucks[k].placeItem(items[i].width, items[i].length, x, y);
                            assignment[i] = k;
                            xCoord[i] = x;
                            yCoord[i] = y;
                            rotation[i] = 0;
                            placed = true;
                        } else if (trucks[k].canPlaceItem(items[i].length, items[i].width, x, y)) {
                            trucks[k].placeItem(items[i].length, items[i].width, x, y);
                            assignment[i] = k;
                            xCoord[i] = x;
                            yCoord[i] = y;
                            rotation[i] = 1;
                            placed = true;
                        }
                    }
                }
            }
        }

        // Tính chi phí ban đầu và sao lưu trạng thái tốt nhất
        int bestCost = calculateCost(assignment, trucks);
        int[] bestAssignment = assignment.clone();
        int[] bestXCoord = xCoord.clone();
        int[] bestYCoord = yCoord.clone();
        int[] bestRotation = rotation.clone();
        
        for (int it = 0; it < maxIter; it++) {
            for (int i = 0; i < items.length; i++) {
                int oldTruck = assignment[i];
                int oldX = xCoord[i];
                int oldY = yCoord[i];
                int oldRotation = rotation[i];

                if (oldRotation == 0) {
                    trucks[oldTruck].removeItem(items[i].width, items[i].length, oldX, oldY);
                } else {
                    trucks[oldTruck].removeItem(items[i].length, items[i].width, oldX, oldY);
                }
                
                // Chọn ngẫu nhiên một xe tải và vị trí mới để đặt món hàng
                int newTruck = r.nextInt(trucks.length);
                int newX = r.nextInt(trucks[newTruck].width);
                int newY = r.nextInt(trucks[newTruck].length);
                int newRotation = r.nextInt(2);

                boolean canPlace = false;
                if (newRotation == 0 && trucks[newTruck].canPlaceItem(items[i].width, items[i].length, newX, newY)) {
                    trucks[newTruck].placeItem(items[i].width, items[i].length, newX, newY);
                    canPlace = true;
                } else if (newRotation == 1 && trucks[newTruck].canPlaceItem(items[i].length, items[i].width, newX, newY)) {
                    trucks[newTruck].placeItem(items[i].length, items[i].width, newX, newY);
                    canPlace = true;
                }

                if (canPlace) {
                    assignment[i] = newTruck;
                    xCoord[i] = newX;
                    yCoord[i] = newY;
                    rotation[i] = newRotation;
                } else {
                    // Hoàn trả món hàng về vị trí cũ nếu không thể đặt vào vị trí mới
                    if (oldRotation == 0) {
                        trucks[oldTruck].placeItem(items[i].width, items[i].length, oldX, oldY);
                    } else {
                        trucks[oldTruck].placeItem(items[i].length, items[i].width, oldX, oldY);
                    }
                }

                // Tính toán chi phí hiện tại và cập nhật trạng thái tốt nhất nếu cần
                int currentCost = calculateCost(assignment, trucks);
                if (currentCost < bestCost || r.nextDouble() < Math.exp((bestCost - currentCost) / temperature)) {
                    bestCost = currentCost;
                    bestAssignment = assignment.clone();
                    bestXCoord = xCoord.clone();
                    bestYCoord = yCoord.clone();
                    bestRotation = rotation.clone();
                } else {
                    assignment[i] = oldTruck;
                    xCoord[i] = oldX;
                    yCoord[i] = oldY;
                    rotation[i] = oldRotation;
                }
            }
            temperature = updateTemperature(temperature, coolingRate);
        }

        // Tạo danh sách các giải pháp từ trạng thái tốt nhất tìm được
        for (int i = 0; i < items.length; i++) {
            solutions.add(new Solution(bestAssignment[i] + 1, bestXCoord[i], bestYCoord[i], bestRotation[i]));
        }

        return solutions;
    }

    private static int calculateCost(int[] assignment, Truck[] trucks) {
        boolean[] used = new boolean[trucks.length];
        int totalCost = 0;
        for (int truck : assignment) {
            if (!used[truck]) {
                totalCost += trucks[truck].cost;
                used[truck] = true;
            }
        }
        return totalCost;
    }

    private static double initTemperature() {
        return 10000;
    }

    // Cập nhật nhiệt độ sau mỗi lần lặp
    private static double updateTemperature(double t, double coolingRate) {
        return t * (1 - coolingRate);
    }
}
