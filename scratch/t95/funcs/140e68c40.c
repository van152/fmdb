// THUNK ALIAS -> sub_143C3A8C0 (jmp:0x140e68c40->0x143c3a8c0)
_QWORD *__fastcall sub_143C3A8C0(_QWORD *a1)
{
  __int64 *v2; // rcx
  __int64 *v3; // rdx
  int v4; // ebx
  _QWORD *v5; // rax
  __int64 v6; // rdi
  unsigned int v7; // esi
  _QWORD *v8; // r15
  __int64 *v9; // rbx
  __int64 *v10; // rbp
  __int64 v11; // r14
  char v12; // r12
  __int64 v13; // rdi
  _QWORD *v14; // rax
  _QWORD *v15; // rcx
  __int64 v16; // rdi
  char v17; // cl
  _QWORD *v18; // rdx
  __int64 v19; // rcx
  __int64 v20; // rdx
  int v21; // ebx
  unsigned int v22; // edi
  __int64 v23; // rcx
  __int64 v24; // rdx
  int v25; // ebx
  unsigned int v26; // edi

  v2 = (__int64 *)a1[35];
  v3 = (__int64 *)a1[36];
  if ( v2 == v3 )
  {
    v5 = nullptr;
  }
  else
  {
    v4 = 1049072;
    v5 = nullptr;
    while ( 1 )
    {
      v6 = *v2;
      if ( *(_QWORD **)(*v2 + 8) == a1 )
      {
        v7 = *(unsigned __int8 *)(v6 + 48);
        if ( v7 <= 0x14 )
        {
          if ( _bittest(&v4, v7) )
            break;
        }
      }
      if ( ++v2 == v3 )
        goto LABEL_9;
    }
    v5 = *(_QWORD **)v6;
  }
LABEL_9:
  v8 = v5;
  if ( v5 == nullptr )
    v8 = a1;
  v9 = (__int64 *)v8[6];
  v10 = (__int64 *)v8[7];
  v11 = 0;
  if ( v9 == v10 )
    return (_QWORD *)v11;
  if ( v5 != nullptr )
  {
    v12 = 0;
    while ( 1 )
    {
      v13 = *v9;
      v14 = *(_QWORD **)(*v9 + 48);
      v15 = v14 + 46;
      if ( *(_BYTE *)(*v9 + 47) == 0 )
        v15 = v14 + 27;
      if ( *v15 != 0 )
      {
        if ( v14 == a1 )
          goto LABEL_14;
      }
      else
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) != 0 )
          goto LABEL_15;
        v14 = *(_QWORD **)(v13 + 48);
        if ( v14 == a1 )
        {
LABEL_14:
          v12 = 1;
          goto LABEL_15;
        }
      }
      if ( (v12 & 1) != 0 )
      {
        v11 = 0;
        if ( *(_BYTE *)(v13 + 47) != 0 || v14 == nullptr )
          return (_QWORD *)v11;
        v23 = v8[35];
        v24 = v8[36];
        if ( v23 != v24 )
        {
          v25 = 1049072;
          v11 = 0;
          while ( 1 )
          {
            if ( *(_QWORD **)(*(_QWORD *)v23 + 8LL) == v14 )
            {
              v26 = *(unsigned __int8 *)(*(_QWORD *)v23 + 48LL);
              if ( v26 <= 0x14 )
              {
                if ( _bittest(&v25, v26) )
                  break;
              }
            }
            v23 += 8;
            if ( v23 == v24 )
              return (_QWORD *)v11;
          }
          return v14;
        }
        return nullptr;
      }
LABEL_15:
      if ( ++v9 == v10 )
        return (_QWORD *)v11;
    }
  }
  while ( 1 )
  {
    v16 = *v9;
    v17 = *(_BYTE *)(*v9 + 47);
    v14 = *(_QWORD **)(*v9 + 48);
    v18 = v14 + 46;
    if ( v17 == 0 )
      v18 = v14 + 27;
    if ( *v18 != 0 )
      break;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) == 0 )
    {
      v17 = *(_BYTE *)(v16 + 47);
      v14 = *(_QWORD **)(v16 + 48);
      break;
    }
    if ( ++v9 == v10 )
      return (_QWORD *)v11;
  }
  v11 = 0;
  if ( v17 != 0 || v14 == nullptr )
    return (_QWORD *)v11;
  v19 = a1[35];
  v20 = a1[36];
  if ( v19 == v20 )
    return nullptr;
  v21 = 1049072;
  v11 = 0;
  do
  {
    if ( *(_QWORD **)(*(_QWORD *)v19 + 8LL) == v14 )
    {
      v22 = *(unsigned __int8 *)(*(_QWORD *)v19 + 48LL);
      if ( v22 <= 0x14 )
      {
        if ( _bittest(&v21, v22) )
          return v14;
      }
    }
    v19 += 8;
  }
  while ( v19 != v20 );
  return (_QWORD *)v11;
}
