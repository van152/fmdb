// THUNK ALIAS -> sub_143C17300 (jmp:0x140e58460->0x143c17300)
char __fastcall sub_143C17300(_QWORD *a1)
{
  _QWORD *v2; // rbx
  _QWORD *v3; // rdi
  _QWORD *v4; // rsi
  __int64 v5; // rsi
  char result; // al
  unsigned __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rbx
  signed __int32 v10; // et0

  v2 = (_QWORD *)*a1;
  v3 = (_QWORD *)a1[1];
  if ( (_QWORD *)*a1 != v3 )
  {
    v4 = (_QWORD *)*a1;
    do
    {
      if ( *v4 != 0 )
        sub_140DD5820();
      ++v4;
    }
    while ( v4 != v3 );
    v5 = a1[1] - (_QWORD)v3;
    result = sub_141758A00();
    a1[1] = (char *)v2 + v5;
    v3 = (_QWORD *)*a1;
  }
  if ( v3 != nullptr )
  {
    v7 = a1[2] - (_QWORD)v3;
    if ( v7 == -1 )
    {
      v7 = *(unsigned int *)((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_17;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v8 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v8) >> 3 > v7 )
    {
      v9 = *(_QWORD *)(v8 + 8 * v7);
      if ( v9 != 0 )
      {
        MEMORY[0x1419475D8](v9 + 32, (char *)v3 - *(unsigned int *)(v9 + 120));
        if ( *(_BYTE *)(v9 + 72) != 0 )
        {
          v10 = _InterlockedDecrement((volatile signed __int32 *)(v9 + 64));
          result = v10 != 0;
          if ( v10 != 0 )
            goto LABEL_18;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v9 + 97) != 0 )
          result = sub_1412D33C0(v9);
        goto LABEL_18;
      }
    }
LABEL_17:
    result = MEMORY[0x141948990]((char *)v3 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_18:
    a1[2] = 0;
    a1[1] = 0;
    *a1 = 0;
  }
  return result;
}
