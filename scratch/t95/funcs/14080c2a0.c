int **__fastcall sub_14080C2A0(int **a1, int **a2, int a3)
{
  int *v5; // rax
  int v6; // r15d
  unsigned int v7; // ebp
  unsigned int v8; // esi
  __int64 v9; // rcx
  int v10; // ebx
  int *v11; // rdi
  __int64 v12; // rcx
  int v13; // esi
  int *v14; // rax
  int v15; // esi
  int v16; // ebp
  __int64 v17; // r15
  int v18; // eax
  _BYTE *v19; // r12

  v5 = *a1;
  v6 = 0;
  v7 = 0;
  if ( *a1 != nullptr )
    v7 = *v5;
  v8 = a3 - 1;
  v9 = (__int64)(v5 + 1);
  if ( v5 == nullptr )
    v9 = 0x1419435F1LL;
  v10 = sub_140810720(v9, v7, 0);
  v11 = *a1;
  v12 = (__int64)(*a1 + 1);
  if ( *a1 == nullptr )
    v12 = 0x1419435F1LL;
  v13 = sub_1408108A0(v12, v7, v8);
  if ( v11 != nullptr )
    v6 = *v11;
  v14 = nullptr;
  if ( v10 < 0 || v13 < v10 || v6 <= v10 )
    goto LABEL_26;
  if ( v6 - 1 < v13 )
    v13 = v6 - 1;
  v15 = v13 - v10;
  v16 = v15 + 1;
  if ( v15 + 1 != v6 )
  {
    v17 = sub_1412EC810(264, (unsigned int)v16);
    *(_DWORD *)v17 = 0;
    v18 = 0;
    if ( v16 > 0 )
      v18 = v15 + 1;
    *(_DWORD *)(v17 + 4) = v18;
    v19 = (_BYTE *)(v17 + 8);
    *(_BYTE *)(v17 + 8) = 0;
    if ( v15 < 0 )
    {
      if ( v15 != -1 )
        goto LABEL_24;
    }
    else
    {
      sub_141758A00();
      v19 += (unsigned int)v16;
    }
    *v19 = 0;
LABEL_24:
    v11 = (int *)(v17 + 4);
    *a2 = nullptr;
    goto LABEL_25;
  }
  *a2 = nullptr;
  if ( a2 != a1 )
  {
    if ( v11 == nullptr )
    {
      v14 = nullptr;
      goto LABEL_26;
    }
    v17 = (__int64)(v11 - 1);
LABEL_25:
    _InterlockedIncrement((volatile signed __int32 *)v17);
    v14 = v11;
LABEL_26:
    *a2 = v14;
  }
  return a2;
}
