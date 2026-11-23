char __fastcall sub_143C26F50(__int64 a1, __int64 a2)
{
  int v2; // ebp
  __int64 v3; // r10
  __int64 **v4; // rbx
  __int64 **v5; // r11
  bool v6; // r9
  __int64 **v7; // rcx
  __int64 *v8; // rsi
  unsigned int v9; // eax
  __int64 v10; // r8
  __int64 v11; // rax
  __int64 v12; // rbp
  __int64 *v13; // rcx
  __int64 *v14; // rsi
  __int64 *v15; // rax
  unsigned int v16; // edi
  char v17; // r14
  __int64 v18; // r15
  __int64 v19; // rax
  char v20; // al
  char v21; // cl
  char result; // al
  __int64 *v23; // rsi
  __int64 v24; // rcx
  __int64 v25; // rbp
  int v26; // eax
  int v27; // eax

  v2 = 1049072;
  while ( 2 )
  {
    v3 = a1;
    v4 = *(__int64 ***)(a1 + 280);
    v5 = *(__int64 ***)(a1 + 288);
    v6 = v4 == v5;
    if ( v4 == v5 )
    {
      v6 = true;
      v5 = *(__int64 ***)(a1 + 280);
    }
    else
    {
      v7 = *(__int64 ***)(a1 + 280);
      while ( 1 )
      {
        v8 = *v7;
        if ( (*v7)[1] == v3 )
        {
          v9 = *((unsigned __int8 *)v8 + 48);
          if ( v9 <= 0x14 )
          {
            if ( _bittest(&v2, v9) )
              break;
          }
        }
        if ( ++v7 == v5 )
        {
          v6 = false;
          goto LABEL_11;
        }
      }
      a1 = *v8;
      if ( *v8 != 0 )
        continue;
    }
    break;
  }
LABEL_11:
  v10 = 1049072;
  v11 = v3;
LABEL_12:
  v12 = v11;
  v13 = *(__int64 **)(v11 + 280);
  v14 = *(__int64 **)(v11 + 288);
  while ( v13 != v14 )
  {
    v15 = (__int64 *)*v13;
    if ( *(_QWORD *)(*v13 + 8) == v12 )
    {
      v16 = *((unsigned __int8 *)v15 + 48);
      if ( v16 <= 0x14 )
      {
        if ( _bittest((const int *)&v10, v16) )
        {
          v11 = *v15;
          if ( v11 != 0 )
            goto LABEL_12;
          break;
        }
      }
    }
    ++v13;
  }
  v17 = *(_BYTE *)(*(_QWORD *)(v12 + 256) + 301LL);
  v18 = 0;
  if ( !v6 )
  {
    v10 = *(unsigned __int8 *)(*(_QWORD *)(v12 + 256) + 301LL);
    do
    {
      v23 = *v4;
      v24 = **v4;
      if ( v24 != 0 )
      {
        v25 = v23[1];
        if ( v25 != 0 )
        {
          v26 = *((unsigned __int8 *)v23 + 48);
          if ( (unsigned int)(v26 - 4) >= 5 && v26 != 20 )
          {
            v27 = *((_DWORD *)v23 + 7);
            if ( (v27 & 0x400) != 0 && v25 == v3 || (v27 & 0x10000) != 0 && v25 == v3 )
              v10 = *(unsigned __int8 *)(*(_QWORD *)(v24 + 256) + 301LL);
            if ( (char)v10 > v17 )
            {
              v18 = *(_QWORD *)(v24 + 336);
              v17 = v10;
            }
          }
        }
      }
      ++v4;
    }
    while ( v4 != v5 );
  }
  if ( v18 == 0 )
    v18 = *(_QWORD *)(v3 + 336);
  if ( (_BYTE)a2 != 0
    && v17 >= 0
    && v18 != 0
    && (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v18 + 56LL))(v18, a2, v10) == 1 )
  {
    v19 = sub_141758910(v18, 0, &unk_141AADA20, &unk_141AADA50, 0);
    if ( v19 != 0 )
    {
      v20 = *(_BYTE *)(v19 + 2227);
      v21 = v17;
      if ( v20 > v17 )
        v21 = v20;
      v17 = v21;
    }
  }
  result = 1;
  if ( v17 <= 19 )
  {
    result = 2;
    if ( v17 <= 16 )
    {
      result = 3;
      if ( v17 <= 14 )
      {
        result = 4;
        if ( v17 <= 11 )
        {
          result = 5;
          if ( v17 <= 8 )
          {
            result = 6;
            if ( v17 <= 5 )
            {
              result = 7;
              if ( v17 <= 2 )
                return ((unsigned __int8)v17 >> 7) | 8;
            }
          }
        }
      }
    }
  }
  return result;
}
