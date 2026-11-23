unsigned __int64 __fastcall sub_140893BE0(__int64 *a1, unsigned __int64 a2)
{
  __int64 v2; // r15
  unsigned __int64 result; // rax
  __int64 v6; // r13
  __int64 v7; // r12
  __int64 v8; // rbx
  unsigned __int64 v9; // rcx
  __int64 v10; // r8
  __int64 v11; // r14

  v2 = *a1;
  result = (a1[2] - *a1) >> 3;
  if ( result < a2 )
  {
    if ( a2 >> 61 != 0 )
      sub_1400526C0();
    v6 = a1[1];
    v7 = sub_1407E4490(qword_141ABD470, 8 * a2);
    sub_141758A00();
    v8 = *a1;
    if ( *a1 == 0 )
      goto LABEL_14;
    v9 = a1[2] - v8;
    if ( v9 == -1 )
    {
      v9 = *(unsigned int *)(v8 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_13;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_13;
    }
    v10 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v10) >> 3 > v9 )
    {
      v11 = *(_QWORD *)(v10 + 8 * v9);
      if ( v11 != 0 )
      {
        MEMORY[0x1419475D8](v11 + 32, v8 - *(unsigned int *)(v11 + 120));
        if ( (*(_BYTE *)(v11 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v11 + 64)) == 0)
          && *(_BYTE *)(v11 + 97) != 0 )
        {
          sub_1412D33C0(v11);
        }
        goto LABEL_14;
      }
    }
LABEL_13:
    MEMORY[0x141948990](v8 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_14:
    *a1 = v7;
    a1[1] = v7 + v6 - v2;
    result = v7 + 8 * a2;
    a1[2] = result;
  }
  return result;
}
