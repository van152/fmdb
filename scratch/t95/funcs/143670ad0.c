_QWORD *__fastcall sub_143670AD0(_QWORD *a1)
{
  unsigned __int64 v1; // rdx
  __int64 v2; // rdi
  __int64 v3; // rsi
  __int64 v4; // rsi
  unsigned __int64 v5; // rsi
  __int64 v6; // r14
  __int64 v7; // rcx
  unsigned __int64 v8; // rcx
  __int128 v11; // [rsp+30h] [rbp-20h] BYREF
  __int64 v12; // [rsp+40h] [rbp-10h]
  __int64 v13; // [rsp+48h] [rbp-8h]

  v13 = -2;
  *(_QWORD *)((char *)a1 + 45) = 0;
  a1[5] = 0;
  a1[4] = 0;
  a1[3] = 0;
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v11 = 0;
  v12 = 0;
  if ( (unsigned __int8)sub_1412D3A30(0x1418F05C3LL, &v11) == 0 )
  {
    v1 = v12 - v11;
    if ( (unsigned __int64)(v12 - v11) > 0x127 )
    {
      v5 = *((_QWORD *)&v11 + 1) - v11;
      if ( *((_QWORD *)&v11 + 1) - (_QWORD)v11 > 0x127u )
      {
        v4 = v11 + 296;
        sub_1417589F0();
      }
      else
      {
        sub_1417589F0();
        v6 = *((_QWORD *)&v11 + 1);
        sub_1417589F0();
        v4 = v6 + 8 * (37 - (v5 >> 3));
      }
    }
    else
    {
      v2 = 37;
      if ( (v1 >> 3) + (v1 >> 4) >= 0x26 )
        v2 = (v1 >> 3) + (v1 >> 4);
      if ( (_QWORD)v11 != 0 )
      {
        sub_141750D04(v11);
        v11 = 0;
        v12 = 0;
      }
      v3 = sub_141750CC0(8 * v2);
      *(_QWORD *)&v11 = v3;
      v12 = v3 + 8 * v2;
      sub_1417589F0();
      v4 = v3 + 296;
    }
    *((_QWORD *)&v11 + 1) = v4;
  }
  sub_1407E4080(a1, &v11);
  v7 = v11;
  if ( (_QWORD)v11 != 0 )
  {
    if ( (unsigned __int64)(v12 - v11) >= 0x1000 )
    {
      v8 = v11 - 8 - *(_QWORD *)(v11 - 8);
      if ( v8 >= 0x20 )
        MEMORY[0x1419488E8](v8);
      v7 = *(_QWORD *)(v11 - 8);
    }
    sub_141750D04(v7);
  }
  return a1;
}
