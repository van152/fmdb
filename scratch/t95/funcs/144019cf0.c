int *__fastcall sub_144019CF0(__int64 a1, int *a2, int a3, char a4, char a5, unsigned __int8 a6, __int64 a7)
{
  bool v11; // r13
  int v12; // edx
  char v13; // di
  int v14; // r9d
  int v15; // esi
  int v16; // ebx
  __m128 v17; // xmm2
  __m128 v18; // xmm3
  __m128 v19; // xmm0
  __m128 v20; // xmm1
  float v21; // xmm1_4
  bool v22; // zf
  int v23; // eax
  __m128 v24; // xmm1
  __m128 v25; // xmm1
  int v26; // ecx
  int v28; // [rsp+58h] [rbp-60h] BYREF
  __int128 v29; // [rsp+60h] [rbp-58h] BYREF
  int v30; // [rsp+70h] [rbp-48h]
  char v31; // [rsp+74h] [rbp-44h]

  v11 = a4 == 3;
  v29 = 0;
  v30 = 0;
  v31 = 1;
  if ( (_BYTE)word_141B60320 != 0 && (_BYTE)word_141B60460 == 6 )
  {
    v12 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5FD40 + 40LL))(qword_141B5FD40, a1);
  }
  else
  {
    v12 = (unsigned __int16)word_141AB0260;
    if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
    {
      word_141AB0260 = 2023;
      LOWORD(v12) = 2023;
    }
  }
  v13 = 2 - v11;
  if ( (unsigned __int8)sub_1411DCE60(a1, v12, a3, a6, (__int64)&v29, a4, a7, 0, 1, 0) != 0 )
  {
    if ( (a4 & 0xFE) == 2 && a5 != 0 )
    {
      v15 = v29;
      v16 = DWORD1(v29);
      LOBYTE(v14) = 1;
      if ( (unsigned __int8)sub_14150DD00(v29, DWORD1(v29), v13, v14, 0) != 0 )
      {
        v19.m128_f32[0] = (float)BYTE2(v16) * MEMORY[0x1417E9400];
        v17.m128_f32[0] = (float)BYTE1(v16) * MEMORY[0x1417E9400];
        v18.m128_f32[0] = (float)(unsigned __int8)v16 * MEMORY[0x1417E9400];
        if ( v17.m128_f32[0] < v19.m128_f32[0] || v18.m128_f32[0] < v19.m128_f32[0] )
        {
          if ( v18.m128_f32[0] >= v17.m128_f32[0] )
          {
            v25 = _mm_cmple_ss(v18, v19);
            LODWORD(v21) = _mm_andnot_ps(v25, v18).m128_u32[0] | v19.m128_i32[0] & v25.m128_i32[0];
            v19.m128_f32[0] = (float)BYTE1(v16) * MEMORY[0x1417E9400];
          }
          else
          {
            v24 = _mm_cmple_ss(v17, v19);
            LODWORD(v21) = _mm_andnot_ps(v24, v17).m128_u32[0] | v19.m128_i32[0] & v24.m128_i32[0];
            v19.m128_f32[0] = (float)(unsigned __int8)v16 * MEMORY[0x1417E9400];
          }
        }
        else
        {
          v20 = _mm_cmple_ss(v18, v17);
          LODWORD(v21) = _mm_andnot_ps(v20, v18).m128_u32[0] | v17.m128_i32[0] & v20.m128_i32[0];
        }
        v26 = -16777216;
        if ( MEMORY[0x14188E524] > (float)((float)(v21 + v19.m128_f32[0]) * MEMORY[0x141764680]) )
          v26 = -1;
        *a2 = v26;
        return a2;
      }
    }
    else
    {
      v15 = v29;
    }
    if ( v15 != 0 )
      *a2 = v15;
    else
      *a2 = -16777216;
    return a2;
  }
  sub_1411DF0C0(a1, &v28, a3, a4, a6, 0);
  v22 = (unsigned __int8)sub_14150DD00(v28, -1, v13, 0, 0) == 0;
  v23 = -16777216;
  if ( v22 )
    v23 = -1;
  *a2 = v23;
  return a2;
}
