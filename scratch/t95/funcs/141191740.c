char __fastcall sub_141191740(_QWORD *a1)
{
  __int64 v2; // rdi
  unsigned __int64 v3; // rcx
  __int64 v4; // rbx
  __int64 v5; // rbx
  signed __int32 v6; // et0
  char result; // al
  _QWORD *v8; // rbx
  _QWORD *v9; // rdi
  _QWORD *v10; // rsi
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  _QWORD *v13; // r14
  __int64 v14; // rdx
  __int64 v15; // rbx
  signed __int32 v16; // et0

  v2 = a1[6];
  if ( v2 != 0 )
  {
    v3 = a1[8] - v2;
    if ( v3 == -1 )
      v3 = *(unsigned int *)(v2 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v4 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v4) >> 3 > v3 )
      {
        v5 = *(_QWORD *)(v4 + 8 * v3);
        if ( v5 != 0 )
        {
          MEMORY[0x1419475D8](v5 + 32, v2 - *(unsigned int *)(v5 + 120));
          if ( *(_BYTE *)(v5 + 72) != 0 )
          {
            v6 = _InterlockedDecrement((volatile signed __int32 *)(v5 + 64));
            result = v6 != 0;
            if ( v6 != 0 )
              goto LABEL_11;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v5 + 97) != 0 )
            result = sub_1412D33C0(v5);
          goto LABEL_11;
        }
      }
    }
    result = MEMORY[0x141948990](v2 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_11:
    a1[8] = 0;
    a1[7] = 0;
    a1[6] = 0;
  }
  v8 = (_QWORD *)a1[3];
  v9 = (_QWORD *)a1[4];
  if ( v8 != v9 )
  {
    v10 = (_QWORD *)a1[3];
    do
    {
      if ( *v10 != 0 )
        sub_141750CFC(*v10);
      ++v10;
    }
    while ( v10 != v9 );
    v11 = a1[4] - (_QWORD)v9;
    result = sub_141758A00();
    a1[4] = (char *)v8 + v11;
    v9 = (_QWORD *)a1[3];
  }
  if ( v9 != nullptr )
  {
    v12 = a1[5] - (_QWORD)v9;
    if ( v12 == -1 )
      v12 = *(unsigned int *)((char *)v9 - *(unsigned int *)(qword_141ABD470 + 48));
    v13 = a1 + 3;
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v14 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v12 )
      {
        v15 = *(_QWORD *)(v14 + 8 * v12);
        if ( v15 != 0 )
        {
          MEMORY[0x1419475D8](v15 + 32, (char *)v9 - *(unsigned int *)(v15 + 120));
          if ( *(_BYTE *)(v15 + 72) != 0 )
          {
            v16 = _InterlockedDecrement((volatile signed __int32 *)(v15 + 64));
            result = v16 != 0;
            if ( v16 != 0 )
              goto LABEL_28;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v15 + 97) != 0 )
            result = sub_1412D33C0(v15);
          goto LABEL_28;
        }
      }
    }
    result = MEMORY[0x141948990]((char *)v9 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_28:
    v13[2] = 0;
    v13[1] = 0;
    *v13 = 0;
  }
  return result;
}
