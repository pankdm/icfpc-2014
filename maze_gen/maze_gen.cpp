#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <queue>

using namespace std;

int my_rand(int mod) {
    return rand() % mod;
}

class MazeBuilder {
public:
    MazeBuilder(size_t height, size_t width)
        : height(height)
        , width(width)
        , success(false)
    { /* no-op */ }

    bool succeeded() const {
        return success;
    }

    vector<string> genMaze(int ghosts, double pills = 0.2, double power = 0.25) {
        vector<string> maze = genWalls();

        vector< pair<int, int> > freeCells;
        for (size_t i = 0; i != height; ++i)
            for (size_t j = 0; j != width; ++j)
                if (maze[i][j] == ' ')
                    freeCells.push_back(make_pair(i, j));
        if (2 + ghosts > freeCells.size()) {
            success = false;
            return maze;
        }

        random_shuffle(freeCells.begin(), freeCells.end(), my_rand);
        maze[freeCells[0].first][freeCells[0].second] = '\\';
        maze[freeCells[1].first][freeCells[1].second] = '%';
        int ind = 2;
        for (int i = 0; i < ghosts; ++i, ++ind)
            maze[freeCells[ind].first][freeCells[ind].second] = '=';

        int pillsCnt = (freeCells.size() - 2 - ghosts) * pills;
        int powerCnt = pillsCnt * power;
        pillsCnt -= powerCnt;
        for (int i = 0; i < pillsCnt; ++i, ++ind)
            maze[freeCells[ind].first][freeCells[ind].second] = '.';
        for (int i = 0; i < powerCnt; ++i, ++ind)
            maze[freeCells[ind].first][freeCells[ind].second] = 'o';

        return maze;
    }

    vector<string> genWalls() {
        vector<string> maze(height, string(width, ' '));
        for (size_t i = 0; i != height; ++i)
            maze[i][0] = maze[i][width - 1] = '#';
        for (size_t j = 1; j != width; ++j)
            maze[0][j] = maze[height - 1][j] = '#';

        vector<int> perm(4);
        for (size_t i = 0; i != 4; ++i)
            perm[i] = i;

        success = true;
        while (true) {
            int bad_i = -1, bad_j = -1;
            for (size_t i = 0; i + 1 != height; ++i)
                for (size_t j = 0; j + 1 != width; ++j) {
                    if (maze[i][j] != '#' && maze[i][j + 1] != '#' &&
                        maze[i + 1][j] != '#' && maze[i + 1][j + 1] != '#')
                    {
                        bad_i = i, bad_j = j;
                    }
                }
             if (bad_i == -1 || bad_j == -1)
                 break;
            
            bool modified = false;
            random_shuffle(perm.begin(), perm.end(), my_rand);
            for (size_t i = 0; i != 4; ++i) {
                int d = perm[i];
                int d_i = d & 1, d_j = (d >> 1) & 1;
                if (blockIfPossible(maze, bad_i + d_i, bad_j + d_j)) {
                    modified = true;
                    break;
                }
            }
            if (!modified) {
                cerr << bad_i << ' ' << bad_j << '\n';
                success = false;
                break;
            }
        }

        return maze;
    }

    bool blockIfPossible(vector<string>& maze, int x, int y) {
        char oldChar = maze[x][y];
        maze[x][y] = '#';

        int good_i = -1, good_j = -1;
        bool found_good = false;
        for (size_t i = 1; i != height && !found_good; ++i)
            for (size_t j = 1; j != width && !found_good; ++j)
                if (maze[i][j] != '#') {
                    good_i = i, good_j = j;
                    found_good = true;
                }

        if (!isConnected(maze, good_i, good_j)) {
            maze[x][y] = oldChar;
            return false;
        }
        return true;
    }

    bool isConnected(const vector<string>& maze, int x, int y) {
        static const int dirs[4][2] = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} };

        queue< pair<int, int> > q;
        q.push(make_pair(x, y));
        vector< vector<bool> > visited(height, vector<bool>(width));
        visited[x][y] = true;
        int visited_count = 1;
        while (!q.empty()) {
            const pair<int, int>& p = q.front(); q.pop();
            for (size_t i = 0; i != 4; ++i) {
                int new_x = p.first + dirs[i][0], new_y = p.second + dirs[i][1];
                if (new_x < 0 || new_y < 0 || new_x >= height || new_y >= width)
                    continue;
                if (!visited[new_x][new_y] && maze[new_x][new_y] != '#') {
                    visited[new_x][new_y] = true;
                    ++visited_count;
                    q.push(make_pair(new_x, new_y));
                }
            }
        }

        for (size_t i = 0; i != height; ++i)
            for (size_t j = 0; j != width; ++j)
                if (maze[i][j] != '#')
                    --visited_count;
        return visited_count == 0;
    }

private:
    size_t height;
    size_t width;
    bool success;
};

int main(int argc, char** argv) {
    srand(time(0));

    if (argc < 6) {
        printf("Usage: %s <height> <width> <ghosts> <pill_ratio> <power_ratio> [output]\n", argv[0]);
        return 1;
    }
    size_t height = atol(argv[1]);
    size_t width = atol(argv[2]);
    int ghosts = atol(argv[3]);
    double pills = atof(argv[4]);
    double powerPills = atof(argv[5]);
    ostream* output = &cout;
    if (argc >= 7) {
        output = new ofstream(argv[6]);
    }

    MazeBuilder builder(height, width);
    const vector<string>& maze = builder.genMaze(ghosts, pills, powerPills);
    if (!builder.succeeded())
        cerr << "FUCK!\n";
    for (size_t i = 0; i != height; ++i) {
        for (size_t j = 0; j != width; ++j)
            *output << maze[i][j];
        *output << endl;
    }
    if (output != &cout)
        delete output;

    return 0;
}

