int **__fastcall sub_1436E3220(int **a1, __int64 a2, int a3)
{
  int v3; // r12d
  int v5; // ebx
  int v6; // edi
  __int64 v7; // rax
  volatile signed __int32 *v8; // r13
  _BYTE *v9; // rsi
  _BYTE *v10; // rbx
  unsigned int v11; // eax
  bool v12; // zf
  _BYTE *v13; // rsi
  volatile signed __int32 *v14; // rcx

  v3 = a3;
  if ( a3 == -1 )
  {
    v3 = sub_141758DB0(a2);
    if ( v3 <= 0 )
      return a1;
  }
  else if ( a3 <= 0 )
  {
    return a1;
  }
  v5 = 0;
  v6 = 0;
  if ( *a1 != nullptr )
    v6 = **a1;
  v7 = sub_1412EC810(264, (unsigned int)(v6 + v3));
  v8 = (volatile signed __int32 *)v7;
  *(_DWORD *)v7 = 0;
  if ( v6 + v3 > 0 )
    v5 = v6 + v3;
  *(_DWORD *)(v7 + 4) = v5;
  v9 = (_BYTE *)(v7 + 8);
  *(_BYTE *)(v7 + 8) = 0;
  if ( v6 > 0 )
  {
    sub_141758A00();
    v10 = &v9[v6];
LABEL_11:
    *v10 = 0;
    v11 = v6;
    goto LABEL_13;
  }
  v11 = 0;
  v10 = v9;
  v12 = v6 == 0;
  v6 = 0;
  if ( v12 )
    goto LABEL_11;
LABEL_13:
  v13 = &v9[v11];
  sub_141758A00();
  v13[v3] = 0;
  v14 = *a1 - 1;
  if ( *a1 != nullptr && _InterlockedDecrement(v14) == 0 )
    sub_1412EC9A0((__int64)v14);
  *a1 = nullptr;
  _InterlockedIncrement(v8);
  *a1 = (int *)(v8 + 1);
  return a1;
}
