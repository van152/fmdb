__int64 __fastcall sub_141405B90(_DWORD *a1, __int64 a2, _QWORD *a3, _QWORD *a4, char a5)
{
  __int64 v9; // rcx
  __int64 *v10; // rax
  __int64 *v11; // rdx
  __int64 result; // rax
  __int64 v13; // rcx
  __int64 v14; // rdi
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v17; // rsi
  __int64 v18; // rcx
  __int64 v19; // rcx
  __int64 v20; // rsi
  __int64 v21; // rcx
  __int64 v22; // rcx
  __int64 v23; // rsi
  __int64 v24; // rcx
  __int64 v25; // rcx
  int v26; // esi
  __int64 v27; // rax
  __int64 v28; // rsi
  __int64 v29; // rcx
  __int64 v30; // rcx
  __int64 v31; // rsi
  int v32; // eax
  __int64 *v33; // rcx
  __int64 *v34; // rdx
  _QWORD v35[3]; // [rsp+28h] [rbp-38h] BYREF
  __int64 v36; // [rsp+40h] [rbp-20h] BYREF
  __int64 v37; // [rsp+48h] [rbp-18h]
  __int64 v38[8]; // [rsp+50h] [rbp-10h] BYREF

  v38[1] = -2;
  v9 = qword_141B60C30;
  v10 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v9 != 1766410053 )
    {
      v9 += 16;
      if ( v9 == qword_141B60C38 )
        goto LABEL_8;
    }
    if ( v9 == qword_141B60C38 )
      v10 = nullptr;
    else
      v10 = *(__int64 **)(v9 + 8);
  }
LABEL_8:
  v11 = &qword_141B5A4A0;
  if ( v10 != nullptr )
    v11 = v10;
  result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 48LL))(*v11);
  if ( (_BYTE)result != 0 )
  {
    result = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 8LL * (*a3 != *a4) + 32))(
               *a3,
               a3,
               a4);
    if ( (_BYTE)result == 0 )
    {
      result = sub_1400015B0();
      if ( (_BYTE)result == 0 )
      {
        sub_1407C9510(v35);
        v14 = sub_14083D4F0(v13);
        v38[0] = 0;
        sub_140809040(v38, a2, -1);
        v37 = 0;
        v15 = v38[0];
        if ( v38[0] != 0 )
        {
          _InterlockedIncrement((volatile signed __int32 *)(v38[0] - 4));
          v16 = v38[0];
          v37 = v15;
          v36 = v14 + 136;
          if ( v38[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4)) == 0 )
            sub_1412EC9A0(v16 - 4);
        }
        else
        {
          v36 = v14 + 136;
        }
        v38[0] = 0;
        v17 = sub_1412EC810(264, 4);
        *(_QWORD *)v17 = 0x400000000LL;
        strcpy((char *)(v17 + 8), "type");
        if ( v38[0] != 0 )
        {
          v18 = v38[0] - 4;
          if ( _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4)) == 0 )
            sub_1412EC9A0(v18);
        }
        v38[0] = 0;
        _InterlockedIncrement((volatile signed __int32 *)v17);
        v38[0] = v17 + 4;
        sub_14013B810(v35, v38, &v36);
        v19 = v38[0];
        if ( v38[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4)) == 0 )
          sub_1412EC9A0(v19 - 4);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v36 + 16LL))(v36, &v36);
        v36 = 0;
        v20 = sub_1412EC810(264, 9);
        *(_QWORD *)v20 = 0x900000000LL;
        strcpy((char *)(v20 + 8), "old_value");
        if ( v36 != 0 )
        {
          v21 = v36 - 4;
          if ( _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
            sub_1412EC9A0(v21);
        }
        v36 = 0;
        _InterlockedIncrement((volatile signed __int32 *)v20);
        v36 = v20 + 4;
        sub_14013B810(v35, &v36, a3);
        v22 = v36;
        if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
          sub_1412EC9A0(v22 - 4);
        v36 = 0;
        v23 = sub_1412EC810(264, 9);
        *(_QWORD *)v23 = 0x900000000LL;
        *(_BYTE *)(v23 + 16) = MEMORY[0x141909866];
        *(_QWORD *)(v23 + 8) = MEMORY[0x14190985E];
        *(_BYTE *)(v23 + 17) = 0;
        if ( v36 != 0 )
        {
          v24 = v36 - 4;
          if ( _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
            sub_1412EC9A0(v24);
        }
        v36 = 0;
        _InterlockedIncrement((volatile signed __int32 *)v23);
        v36 = v23 + 4;
        sub_14013B810(v35, &v36, a4);
        v25 = v36;
        if ( v36 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 - 4)) == 0 )
          sub_1412EC9A0(v25 - 4);
        v26 = a1[3];
        v27 = sub_14083D4F0(v25);
        LODWORD(v37) = v26;
        v36 = v27 + 40;
        v38[0] = 0;
        v28 = sub_1412EC810(264, 9);
        *(_QWORD *)v28 = 0x900000000LL;
        strcpy((char *)(v28 + 8), "object_id");
        if ( v38[0] != 0 )
        {
          v29 = v38[0] - 4;
          if ( _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4)) == 0 )
            sub_1412EC9A0(v29);
        }
        v38[0] = 0;
        _InterlockedIncrement((volatile signed __int32 *)v28);
        v38[0] = v28 + 4;
        sub_14013B810(v35, v38, &v36);
        v30 = v38[0];
        if ( v38[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4)) == 0 )
          sub_1412EC9A0(v30 - 4);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v36 + 16LL))(v36, &v36);
        v31 = qword_141ABE000;
        v32 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1) - 1;
        v33 = (__int64 *)&unk_141B639D0;
        switch ( v32 )
        {
          case 0:
            v34 = &qword_141B59EF0;
            if ( a5 == 2 )
              v34 = (__int64 *)&unk_141B639F0;
            v33 = (__int64 *)&unk_141B639E0;
            if ( a5 != 1 )
              v33 = v34;
            break;
          case 2:
            v33 = (__int64 *)&unk_141B639E8;
            break;
          case 8:
            v33 = (__int64 *)&unk_141B639D8;
            break;
          case 24:
            break;
          default:
            v33 = &qword_141B59EF0;
            break;
        }
        v36 = *v33;
        sub_14013B9C0(v31, &v36, v35);
        return sub_14083B0A0(v35);
      }
    }
  }
  return result;
}
