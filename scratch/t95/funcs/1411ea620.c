__int64 __fastcall sub_1411EA620(__int64 a1, int a2, __int64 *a3)
{
  __int64 v3; // rbx
  __int64 v5; // rsi
  __int64 v7; // rsi
  __int16 *v8; // rdi
  __int64 v9; // rcx
  __int64 *v11; // rdi
  __int64 v12; // rax
  __int64 v13; // rcx
  __int16 *v14; // rdi
  __int64 *v15; // rdi
  __int64 v16; // rcx
  __int64 *v17; // rdi
  __int64 v18; // rcx
  __int64 *v19; // rdi
  __int64 v20; // rcx
  __int64 v21; // [rsp+20h] [rbp-10h] BYREF
  _QWORD v22[7]; // [rsp+28h] [rbp-8h] BYREF

  v22[1] = -2;
  v5 = *(_QWORD *)(*(_QWORD *)(a1 + 176) + 8LL) - **(_QWORD **)(a1 + 176);
  if ( v5 == 0 )
  {
LABEL_12:
    LOBYTE(v3) = 1;
    if ( a3 != &qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return (unsigned int)v3;
  }
  v3 = a1;
  v7 = v5 >> 3;
  while ( 1 )
  {
    v8 = *(__int16 **)(**(_QWORD **)(v3 + 176) + 8 * v7 - 8);
    if ( (*(unsigned __int8 (__fastcall **)(__int16 *))(*(_QWORD *)v8 + 56LL))(v8) == 9
      && (*(unsigned int (__fastcall **)(__int16 *))(*(_QWORD *)v8 + 64LL))(v8) == -1
      && (*(unsigned int (__fastcall **)(__int16 *))(*(_QWORD *)v8 + 72LL))(v8) == -1 )
    {
      break;
    }
    if ( --v7 == 0 )
      goto LABEL_12;
  }
  LODWORD(v3) = 0;
  if ( a2 <= 1313302125 )
  {
    if ( a2 <= 1312911460 )
    {
      if ( a2 != 1312908910 )
      {
        if ( a2 == 1312909164 )
        {
          LODWORD(v22[0]) = v8[28];
          v21 = sub_14083D4F0(v9) + 40;
          sub_14083DFA0(a3, &v21);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v21);
LABEL_46:
          LOBYTE(v3) = 1;
          return (unsigned int)v3;
        }
        return (unsigned int)v3;
      }
      v15 = (__int64 *)(v8 + 12);
      v12 = sub_14083D4F0(v9);
      v22[0] = 0;
      if ( v22 != v15 )
      {
        v16 = *v15;
        if ( *v15 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v16 - 4));
        v22[0] = v16;
      }
LABEL_45:
      v21 = v12 + 136;
      sub_14083DFA0(a3, &v21);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v21);
      goto LABEL_46;
    }
    if ( a2 != 1312911461 )
    {
      if ( a2 != 1312912238 )
        return (unsigned int)v3;
      v11 = (__int64 *)(v8 + 16);
      v12 = sub_14083D4F0(v9);
      v22[0] = 0;
      if ( v22 != v11 )
      {
        v13 = *v11;
        if ( *v11 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v13 - 4));
        v22[0] = v13;
      }
      goto LABEL_45;
    }
    v14 = v8 + 4;
LABEL_40:
    sub_140FE72B0(v14, 1348825715, a3);
    goto LABEL_46;
  }
  if ( a2 > 1313304676 )
  {
    if ( a2 == 1313305454 )
    {
      v19 = (__int64 *)(v8 + 24);
      v12 = sub_14083D4F0(v9);
      v22[0] = 0;
      if ( v22 != v19 )
      {
        v20 = *v19;
        if ( *v19 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v20 - 4));
        v22[0] = v20;
      }
      goto LABEL_45;
    }
    if ( a2 != 1313304677 )
      return (unsigned int)v3;
    v14 = v8 + 8;
    goto LABEL_40;
  }
  if ( a2 == 1313302126 )
  {
    v17 = (__int64 *)(v8 + 20);
    v12 = sub_14083D4F0(v9);
    v22[0] = 0;
    if ( v22 != v17 )
    {
      v18 = *v17;
      if ( *v17 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v18 - 4));
      v22[0] = v18;
    }
    goto LABEL_45;
  }
  if ( a2 == 1313302380 )
  {
    LODWORD(v22[0]) = v8[29];
    v21 = sub_14083D4F0(v9) + 40;
    sub_14083DFA0(a3, &v21);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v21);
    goto LABEL_46;
  }
  return (unsigned int)v3;
}
