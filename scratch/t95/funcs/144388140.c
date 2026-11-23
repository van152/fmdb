char __fastcall sub_144388140(__int64 a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // rdx
  unsigned __int64 v8; // rbp
  __int64 v9; // r8

  sub_140F7EC80(a3, a1 + 96, *(_QWORD *)(a3 + 40), a5, 1, 0);
  v7 = *(_QWORD *)(a1 + 48);
  if ( *(_QWORD *)(a1 + 56) != v7 )
  {
    v8 = 0;
    do
    {
      sub_140F7EC80(a3, 16 * v8 + v7, *(_QWORD *)(a3 + 80), a5, 1, 0);
      v7 = *(_QWORD *)(a1 + 48);
      v9 = *(_QWORD *)(a1 + 56);
      if ( *(_QWORD *)(v7 + 16 * v8) == 0 )
      {
        sub_141758A00(16 * v8 + v7, 16 * v8 + v7 + 16, v9 - (16 * v8 + v7 + 16));
        v7 = *(_QWORD *)(a1 + 48);
        v9 = *(_QWORD *)(a1 + 56) - 16LL;
        *(_QWORD *)(a1 + 56) = v9;
        --v8;
      }
      ++v8;
    }
    while ( v8 < (v9 - v7) >> 4 );
  }
  sub_140F80050(a3, a1 + 104, a5);
  return 1;
}
