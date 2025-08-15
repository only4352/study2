import {
  Add as AddIcon,
  CheckCircle as CheckCircleIcon,
  Delete as DeleteIcon,
  Undo as UndoIcon,
} from '@mui/icons-material';
import {
  Box,
  Button,
  Container,
  IconButton,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
  Paper,
  TextField,
  Typography,
} from '@mui/material';
import React, { useState } from 'react';

function App() {
  const [todoText, setTodoText] = useState('');
  const [incompleteTodos, setIncompleteTodos] = useState([
    'MUIでTODOアプリを作成',
    'コンポーネントの学習',
    'スタイリングの習得',
  ]);
  const [completeTodos, setCompleteTodos] = useState(['Reactの基礎学習']);

  // 新しいTODOを追加
  const handleAddTodo = () => {
    if (todoText.trim() === '') return;

    setIncompleteTodos(prev => [...prev, todoText]);
    setTodoText('');
  };

  // 未完了のTODOを完了済みに移動
  const handleComplete = index => {
    const targetTodo = incompleteTodos[index];
    setIncompleteTodos(prev => prev.filter((_, i) => i !== index));
    setCompleteTodos(prev => [...prev, targetTodo]);
  };

  // 完了済みのTODOを未完了に戻す
  const handleUndo = index => {
    const targetTodo = completeTodos[index];
    setCompleteTodos(prev => prev.filter((_, i) => i !== index));
    setIncompleteTodos(prev => [...prev, targetTodo]);
  };

  // TODOを削除
  const handleDelete = (index, isComplete = false) => {
    if (isComplete) {
      setCompleteTodos(prev => prev.filter((_, i) => i !== index));
    } else {
      setIncompleteTodos(prev => prev.filter((_, i) => i !== index));
    }
  };

  return (
    <Container maxWidth='md' sx={{ py: 4 }}>
      <Typography
        variant='h3'
        component='h1'
        gutterBottom
        align='center'
        color='primary'
      >
        MUI TODO アプリ
      </Typography>

      {/* 入力エリア */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Box display='flex' gap={2}>
          <TextField
            fullWidth
            label='新しいTODO'
            variant='outlined'
            value={todoText}
            onChange={e => setTodoText(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && handleAddTodo()}
          />
          <Button
            variant='contained'
            startIcon={<AddIcon />}
            onClick={handleAddTodo}
            sx={{ minWidth: 120 }}
          >
            追加
          </Button>
        </Box>
      </Paper>

      <Box display='flex' gap={3}>
        {/* 未完了のTODO */}
        <Paper elevation={3} sx={{ flex: 1, p: 2 }}>
          <Typography variant='h6' gutterBottom color='primary'>
            未完了のTODO ({incompleteTodos.length})
          </Typography>
          <List>
            {incompleteTodos.map((todo, index) => (
              <ListItem key={`incomplete-${index}`} divider>
                <ListItemText primary={todo} />
                <ListItemSecondaryAction>
                  <IconButton
                    edge='end'
                    color='success'
                    onClick={() => handleComplete(index)}
                    sx={{ mr: 1 }}
                  >
                    <CheckCircleIcon />
                  </IconButton>
                  <IconButton
                    edge='end'
                    color='error'
                    onClick={() => handleDelete(index)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>

        {/* 完了済みのTODO */}
        <Paper elevation={3} sx={{ flex: 1, p: 2 }}>
          <Typography variant='h6' gutterBottom color='success.main'>
            完了済みのTODO ({completeTodos.length})
          </Typography>
          <List>
            {completeTodos.map((todo, index) => (
              <ListItem key={`complete-${index}`} divider>
                <ListItemText
                  primary={todo}
                  sx={{
                    textDecoration: 'line-through',
                    color: 'text.secondary',
                  }}
                />
                <ListItemSecondaryAction>
                  <IconButton
                    edge='end'
                    color='primary'
                    onClick={() => handleUndo(index)}
                    sx={{ mr: 1 }}
                  >
                    <UndoIcon />
                  </IconButton>
                  <IconButton
                    edge='end'
                    color='error'
                    onClick={() => handleDelete(index, true)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
    </Container>
  );
}

export default App;
