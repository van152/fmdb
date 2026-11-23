char __fastcall sub_143C5A690(_QWORD *a1)
{
  _QWORD **v2; // r15
  _QWORD **v3; // rdi
  _QWORD **v4; // rbx
  _QWORD *v5; // rsi
  __int64 v6; // rsi
  char result; // al
  unsigned __int64 v8; // rcx
  __int64 v9; // rdx
  __int64 v10; // rbx
  signed __int32 v11; // et0

  v2 = (_QWORD **)*a1;
  v3 = (_QWORD **)a1[1];
  if ( (_QWORD **)*a1 != v3 )
  {
    v4 = (_QWORD **)*a1;
    do
    {
      v5 = *v4;
      if ( *v4 != nullptr )
      {
        if ( *v5 != 0 )
          sub_140FB3720();
        sub_141750CFC(v5);
      }
      ++v4;
    }
    while ( v4 != v3 );
    v6 = a1[1] - (_QWORD)v3;
    result = sub_141758A00();
    a1[1] = (char *)v2 + v6;
    v3 = (_QWORD **)*a1;
  }
  if ( v3 != nullptr )
  {
    v8 = a1[2] - (_QWORD)v3;
    if ( v8 == -1 )
    {
      v8 = *(unsigned int *)((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_19;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_19;
    }
    v9 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v9) >> 3 > v8 )
    {
      v10 = *(_QWORD *)(v9 + 8 * v8);
      if ( v10 != 0 )
      {
        MEMORY[0x1419475D8](v10 + 32, (char *)v3 - *(unsigned int *)(v10 + 120));
        if ( *(_BYTE *)(v10 + 72) != 0 )
        {
          v11 = _InterlockedDecrement((volatile signed __int32 *)(v10 + 64));
          result = v11 != 0;
          if ( v11 != 0 )
            goto LABEL_20;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v10 + 97) != 0 )
          result = sub_1412D33C0(v10);
        goto LABEL_20;
      }
    }
LABEL_19:
    result = MEMORY[0x141948990]((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_20:
    a1[2] = 0;
    a1[1] = 0;
    *a1 = 0;
  }
  return result;
}
