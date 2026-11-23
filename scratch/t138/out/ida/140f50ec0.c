__int64 __fastcall sub_140F50EC0(
        __int64 a1,
        __int64 *a2,
        int a3,
        int a4,
        char a5,
        char a6,
        char a7,
        unsigned __int8 a8)
{
  int v11; // ebx
  __int64 v12; // rcx
  int *v13; // rdx
  __int64 v14; // rsi
  int v15; // edx
  __int64 *v16; // rdx
  int v18; // [rsp+38h] [rbp-30h] BYREF
  int v19; // [rsp+3Ch] [rbp-2Ch] BYREF

  v11 = a1;
  if ( a7 != 0 )
  {
    if ( (a8 & 0xFE) == 0x12 )
      *(_DWORD *)(a1 + 1368) = -1;
    if ( a8 < 0x11u || a8 == 18 )
    {
      if ( (unsigned int)a8 - 1 >= 0x10 )
      {
        if ( a8 != 18 && a8 != 0 )
          goto LABEL_8;
        v12 = a1 + 1344;
        v19 = -1;
        v13 = &v19;
      }
      else
      {
        v12 = a1 + 1344;
        v18 = -1;
        v13 = &v18;
      }
      sub_14094B000(a1: v12, a2: v13);
    }
  }
LABEL_8:
  if ( dword_141B5E750 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(a1: &dword_141B5E750);
    if ( dword_141B5E750 == -1 )
    {
      qword_141B5E5F0 = (__int64)&qword_141B5A1A0;
      dword_141B5E5F8 = 8;
      qword_141B5E600 = (__int64)&qword_141B5A1F0;
      dword_141B5E608 = 1000004;
      qword_141B5E610 = (__int64)&qword_141B5A238;
      dword_141B5E618 = 1000002;
      qword_141B5E620 = (__int64)&qword_141B5A240;
      dword_141B5E628 = 1000003;
      qword_141B5E630 = (__int64)&qword_141B5A1F8;
      dword_141B5E638 = 6;
      qword_141B5E640 = (__int64)&qword_141B5A200;
      dword_141B5E648 = 18;
      qword_141B5E650 = (__int64)&qword_141B5A1B8;
      dword_141B5E658 = 21;
      qword_141B5E660 = (__int64)&qword_141B5A210;
      dword_141B5E668 = 24;
      qword_141B5E670 = (__int64)&qword_141B5A1E8;
      dword_141B5E678 = 10;
      qword_141B5E680 = (__int64)&qword_141B5A1D8;
      dword_141B5E688 = 11;
      qword_141B5E690 = (__int64)&qword_141B5A1B0;
      dword_141B5E698 = 15;
      qword_141B5E6A0 = (__int64)&qword_141B5A1C8;
      dword_141B5E6A8 = 32;
      qword_141B5E6B0 = (__int64)&qword_141B5A1C0;
      dword_141B5E6B8 = 22;
      qword_141B5E6C0 = (__int64)&qword_141B5A208;
      dword_141B5E6C8 = 19;
      qword_141B5E6D0 = (__int64)&qword_141B5A220;
      dword_141B5E6D8 = 7;
      qword_141B5E6E0 = (__int64)&qword_141B5A1D0;
      dword_141B5E6E8 = 30;
      qword_141B5E6F0 = (__int64)&qword_141B5A248;
      dword_141B5E6F8 = 16;
      qword_141B5E700 = (__int64)&qword_141B5A1A8;
      dword_141B5E708 = 17;
      qword_141B5E710 = (__int64)&qword_141B5A1E0;
      dword_141B5E718 = 25;
      qword_141B5E720 = (__int64)&qword_141B5A228;
      dword_141B5E728 = 12;
      qword_141B5E730 = (__int64)&qword_141B5A230;
      dword_141B5E738 = 1000001;
      qword_141B5E740 = (__int64)&qword_141B5A218;
      dword_141B5E748 = 1000000;
      sub_141750EA0(a1: &dword_141B5E750);
    }
  }
  v14 = *a2;
  if ( *(_QWORD *)qword_141B5E5F0 == v14 )
  {
    v16 = &qword_141B5E5F0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E600 == v14 )
  {
    v16 = &qword_141B5E600;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E610 == v14 )
  {
    v16 = &qword_141B5E610;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E620 == v14 )
  {
    v16 = &qword_141B5E620;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E630 == v14 )
  {
    v16 = &qword_141B5E630;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E640 == v14 )
  {
    v16 = &qword_141B5E640;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E650 == v14 )
  {
    v16 = &qword_141B5E650;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E660 == v14 )
  {
    v16 = &qword_141B5E660;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E670 == v14 )
  {
    v16 = &qword_141B5E670;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E680 == v14 )
  {
    v16 = &qword_141B5E680;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E690 == v14 )
  {
    v16 = &qword_141B5E690;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6A0 == v14 )
  {
    v16 = &qword_141B5E6A0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6B0 == v14 )
  {
    v16 = &qword_141B5E6B0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6C0 == v14 )
  {
    v16 = &qword_141B5E6C0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6D0 == v14 )
  {
    v16 = &qword_141B5E6D0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6E0 == v14 )
  {
    v16 = &qword_141B5E6E0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E6F0 == v14 )
  {
    v16 = &qword_141B5E6F0;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E700 == v14 )
  {
    v16 = &qword_141B5E700;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E710 == v14 )
  {
    v16 = &qword_141B5E710;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E720 == v14 )
  {
    v16 = &qword_141B5E720;
    goto LABEL_58;
  }
  if ( *(_QWORD *)qword_141B5E730 == v14 )
  {
    v16 = &qword_141B5E730;
    goto LABEL_58;
  }
  v15 = 8;
  if ( *(_QWORD *)qword_141B5E740 == v14 )
  {
    v16 = &qword_141B5E740;
LABEL_58:
    v15 = *((_DWORD *)v16 + 2);
  }
  return sub_140F70AD0(a1: v11, a2: v15, a3, a4, a5, a6, a7: a8);
}
