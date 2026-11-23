char __fastcall sub_143C260C0(_QWORD *a1, __int64 a2, __int64 a3, __int64 a4)
{
  int v4; // eax
  _QWORD *v5; // rbp
  unsigned __int64 v6; // rdx
  __int64 *v7; // rbx
  __int64 *v8; // rdi
  __int64 v9; // rbp
  unsigned int v10; // esi
  char v11; // r15
  __int64 **v12; // rbx
  __int64 **v13; // r10
  int v14; // edi
  __int64 *v15; // rax
  __int64 v16; // rsi
  unsigned int v17; // ebp
  _QWORD *v18; // rax
  __int64 v19; // r14
  __int64 *v20; // rax
  __int64 v21; // rsi
  _QWORD *v22; // rdi
  int v23; // ebp
  int v24; // eax
  __int64 v25; // rax
  char v26; // al
  char v27; // cl
  char result; // al

  v4 = 1049072;
  v5 = a1;
LABEL_2:
  v6 = (unsigned __int64)v5;
  v7 = (__int64 *)v5[35];
  v8 = (__int64 *)v5[36];
  while ( v7 != v8 )
  {
    v9 = *v7;
    if ( *(_QWORD *)(*v7 + 8) == v6 )
    {
      v10 = *(unsigned __int8 *)(v9 + 48);
      if ( v10 <= 0x14 )
      {
        if ( _bittest(&v4, v10) )
        {
          v5 = *(_QWORD **)v9;
          if ( v5 != nullptr )
            goto LABEL_2;
          break;
        }
      }
    }
    ++v7;
  }
  v11 = *(_BYTE *)(*(_QWORD *)(v6 + 256) + 300LL);
  if ( v11 < 0 )
    return ((unsigned __int8)v11 >> 7) + 7;
  v12 = (__int64 **)a1[35];
  v13 = (__int64 **)a1[36];
  if ( v12 == v13 )
  {
    v18 = a1;
    goto LABEL_32;
  }
  v14 = 1049072;
  v15 = (__int64 *)a1[35];
  while ( 1 )
  {
    v16 = *v15;
    if ( *(_QWORD **)(*v15 + 8) == a1 )
    {
      v17 = *(unsigned __int8 *)(v16 + 48);
      if ( v17 <= 0x14 )
      {
        if ( _bittest(&v14, v17) )
          break;
      }
    }
    if ( ++v15 == (__int64 *)v13 )
      goto LABEL_17;
  }
  v18 = *(_QWORD **)v16;
  if ( *(_QWORD *)v16 != 0 )
    goto LABEL_32;
LABEL_17:
  a3 = *(unsigned __int8 *)(a1[32] + 299LL);
  v19 = 0;
  a4 = *(unsigned __int8 *)(*(_QWORD *)(v6 + 256) + 300LL);
  do
  {
    v20 = *v12;
    v21 = **v12;
    if ( v21 != 0 )
    {
      v22 = (_QWORD *)v20[1];
      if ( v22 != nullptr )
      {
        v23 = *((unsigned __int8 *)v20 + 48);
        v6 = (unsigned int)(v23 - 4);
        if ( (unsigned int)v6 >= 5 && v23 != 20 )
        {
          v24 = *((_DWORD *)v20 + 7);
          if ( (v24 & 0x400) != 0 && v22 == a1 || (v24 & 0x10000) != 0 && v22 == a1 )
            a4 = *(unsigned __int8 *)(*(_QWORD *)(v21 + 256) + 300LL);
          if ( (char)a4 > (char)a3 )
          {
            v19 = *(_QWORD *)(v21 + 336);
            a3 = (unsigned int)a4;
          }
        }
      }
    }
    ++v12;
  }
  while ( v12 != v13 );
  v18 = a1;
  if ( v19 == 0 )
  {
LABEL_32:
    v19 = v18[42];
    if ( v19 == 0 )
      goto LABEL_38;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64, unsigned __int64, __int64, __int64))(*(_QWORD *)v19 + 56LL))(
         v19,
         v6,
         a3,
         a4) == 1 )
  {
    v25 = sub_141758910(v19, 0, &unk_141AADA20, &unk_141AADA50, 0);
    if ( v25 != 0 )
    {
      v26 = *(_BYTE *)(v25 + 2226);
      v27 = v11;
      if ( v26 > v11 )
        v27 = v26;
      v11 = v27;
    }
  }
LABEL_38:
  result = 1;
  if ( v11 <= 19 )
  {
    result = 2;
    if ( v11 <= 16 )
    {
      result = 3;
      if ( v11 <= 13 )
      {
        result = 4;
        if ( v11 <= 9 )
        {
          result = 5;
          if ( v11 <= 5 )
          {
            result = 6;
            if ( v11 <= 2 )
              return ((unsigned __int8)v11 >> 7) + 7;
          }
        }
      }
    }
  }
  return result;
}
