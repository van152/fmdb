bool __fastcall sub_1443AB4F0(__int64 a1, __int64 *a2, __int64 a3)
{
  __int64 v5; // rsi
  float v6; // xmm1_4
  float v7; // xmm0_4
  float v8; // xmm1_4
  int v9; // edi

  v5 = *a2;
  if ( *a2 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 20, a3: 4);
  if ( a3 != 0 && *(_QWORD *)(a1 + 8) == 0 )
    *(_QWORD *)(a1 + 8) = a3;
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 60, a3: 1);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 57, a3: 3);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 44, a3: 13);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 16, a3: 4);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 24, a3: 20);
  if ( *(float *)(a1 + 24) > MEMORY[0x141876F78] )
    *(_DWORD *)(a1 + 24) = 0;
  v6 = *(float *)(a1 + 32);
  v7 = MEMORY[0x1418B74C0];
  if ( MEMORY[0x1418B74C0] > v6 || v6 > MEMORY[0x141774704] )
    *(_DWORD *)(a1 + 32) = 1065353216;
  v8 = *(float *)(a1 + 36);
  if ( v7 > v8 || v8 > MEMORY[0x141774704] )
    *(_DWORD *)(a1 + 36) = 1065353216;
  v9 = *(_DWORD *)(v5 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v5)(a1: v5, a2: 1);
  return v9 == 0;
}
