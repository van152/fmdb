__int64 sub_1442F6C80()
{
  __int64 **v0; // rax
  __int64 *v1; // rcx
  __int64 *v2; // r9
  __int64 result; // rax
  int v4; // r8d
  __int64 v5; // rsi
  __int64 v6; // rdx
  __int64 v7; // rdx
  unsigned int v8; // edx
  __int64 v9; // r11
  __int16 v10; // r10

  v0 = *(__int64 ***)(qword_141B5FE08 + 128);
  v1 = *v0;
  v2 = v0[1];
  result = 0;
  if ( v1 != v2 )
  {
    v4 = 4102;
    do
    {
      v5 = *v1;
      v6 = *(_QWORD *)(*v1 + 368);
      if ( *(_QWORD *)(v6 + 240) != 0 )
      {
        v7 = *(_QWORD *)(v6 + 248);
        if ( v7 != 0 )
        {
          v8 = *(_DWORD *)(v7 + 12);
          if ( v8 > 0xC || !_bittest(&v4, v8) )
          {
            v9 = *(_QWORD *)(v5 + 24);
            v10 = 1500;
            if ( v9 != *(_QWORD *)(v5 + 32) && *(_QWORD *)v9 != 0 )
              v10 = *(_WORD *)(*(_QWORD *)v9 + 168LL);
            result += (((unsigned int)(26215 * v10) >> 31) + ((26215 * v10) >> 18))
                    * (((unsigned int)(26215 * v10) >> 31) + ((26215 * v10) >> 18));
          }
        }
      }
      ++v1;
    }
    while ( v1 != v2 );
  }
  return result;
}
