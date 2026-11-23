__int64 __fastcall sub_140EE7C20(char a1)
{
  __int64 v1; // rsi

  switch ( a1 )
  {
    case 0:
      if ( dword_141B5CE30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5CE30);
        if ( dword_141B5CE30 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5CDE0,
            a2: 1100128636,
            a3: 4096,
            a4: 184,
            a5: 0,
            a6: 0,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_140DF2670);
          sub_141750EA0(a1: &dword_141B5CE30);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B5CDE0, a2: 184);
      *(_QWORD *)(v1 + 8) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 21) = 0;
      *(_QWORD *)(v1 + 30) = 0;
      *(_QWORD *)(v1 + 38) = 0;
      *(_QWORD *)(v1 + 44) = 0;
      *(_QWORD *)(v1 + 52) = -1;
      *(_QWORD *)(v1 + 60) = 0x76C0001076C0001LL;
      *(_QWORD *)(v1 + 68) = 0x76C0001076C0001LL;
      *(_DWORD *)(v1 + 76) = 0;
      *(_WORD *)(v1 + 80) = 0;
      *(_QWORD *)(v1 + 82) = 4279500900LL;
      *(_BYTE *)(v1 + 90) = 0;
      *(_QWORD *)v1 = 0x141878708LL;
      if ( qword_141ABD470 == 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
          }
        }
        qword_141ABD470 = (__int64)&unk_141B59A68;
      }
      *(_QWORD *)(v1 + 160) = 0x76C000100000000LL;
      *(_QWORD *)(v1 + 152) = 0;
      *(_QWORD *)(v1 + 144) = 0;
      *(_QWORD *)(v1 + 136) = 0;
      *(_QWORD *)(v1 + 128) = 0;
      *(_QWORD *)(v1 + 120) = 0;
      *(_QWORD *)(v1 + 112) = 0;
      *(_QWORD *)(v1 + 104) = 0;
      *(_QWORD *)(v1 + 96) = 0;
      *(_WORD *)(v1 + 172) = 1900;
      *(_DWORD *)(v1 + 168) = 0;
      *(_DWORD *)(v1 + 174) = 0;
      *(_BYTE *)(v1 + 178) = 0;
      *(_WORD *)(v1 + 179) = -255;
      break;
    case 1:
      if ( dword_141ABEDD8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141ABEDD8);
        if ( dword_141ABEDD8 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141ABED88,
            a2: 1100128615,
            a3: 128,
            a4: 232,
            a5: 0,
            a6: 0,
            a7: 128,
            a8: 4096);
          sub_141751048(a1: sub_1400DA0F0);
          sub_141750EA0(a1: &dword_141ABEDD8);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141ABED88, a2: 232);
      sub_14103ACF0(a1: v1);
      break;
    case 2:
      if ( dword_141B5E3B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5E3B0);
        if ( dword_141B5E3B0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5E360,
            a2: 1100128656,
            a3: 128,
            a4: 96,
            a5: 0,
            a6: 0,
            a7: 128,
            a8: 4096);
          sub_141751048(a1: sub_140EF7990);
          sub_141750EA0(a1: &dword_141B5E3B0);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B5E360, a2: 96);
      *(_QWORD *)(v1 + 8) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 21) = 0;
      *(_QWORD *)(v1 + 30) = 0;
      *(_QWORD *)(v1 + 38) = 0;
      *(_QWORD *)(v1 + 44) = 0;
      *(_QWORD *)(v1 + 52) = -1;
      *(_QWORD *)(v1 + 60) = 0x76C0001076C0001LL;
      *(_QWORD *)(v1 + 68) = 0x76C0001076C0001LL;
      *(_DWORD *)(v1 + 76) = 0;
      *(_WORD *)(v1 + 80) = 0;
      *(_QWORD *)(v1 + 82) = 4279500900LL;
      *(_BYTE *)(v1 + 90) = 0;
      *(_QWORD *)v1 = 0x14187ED88LL;
      break;
    case 3:
      if ( dword_141ABF340 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141ABF340);
        if ( dword_141ABF340 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141ABF2F0,
            a2: 1100128702,
            a3: 128,
            a4: 96,
            a5: 0,
            a6: 0,
            a7: 128,
            a8: 4096);
          sub_141751048(a1: sub_1400E6D80);
          sub_141750EA0(a1: &dword_141ABF340);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141ABF2F0, a2: 96);
      *(_QWORD *)(v1 + 8) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 21) = 0;
      *(_QWORD *)(v1 + 30) = 0;
      *(_QWORD *)(v1 + 38) = 0;
      *(_QWORD *)(v1 + 44) = 0;
      *(_QWORD *)(v1 + 52) = -1;
      *(_QWORD *)(v1 + 60) = 0x76C0001076C0001LL;
      *(_QWORD *)(v1 + 68) = 0x76C0001076C0001LL;
      *(_DWORD *)(v1 + 76) = 0;
      *(_WORD *)(v1 + 80) = 0;
      *(_QWORD *)(v1 + 82) = 4279500900LL;
      *(_BYTE *)(v1 + 90) = 0;
      *(_QWORD *)v1 = 0x14187C538LL;
      break;
    case 4:
      if ( dword_141B5E358 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5E358);
        if ( dword_141B5E358 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5E308,
            a2: 1100128650,
            a3: 64,
            a4: 96,
            a5: 0,
            a6: 0,
            a7: 64,
            a8: 4096);
          sub_141751048(a1: sub_140EF7640);
          sub_141750EA0(a1: &dword_141B5E358);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B5E308, a2: 96);
      *(_QWORD *)(v1 + 8) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 21) = 0;
      *(_QWORD *)(v1 + 30) = 0;
      *(_QWORD *)(v1 + 38) = 0;
      *(_QWORD *)(v1 + 44) = 0;
      *(_QWORD *)(v1 + 52) = -1;
      *(_QWORD *)(v1 + 60) = 0x76C0001076C0001LL;
      *(_QWORD *)(v1 + 68) = 0x76C0001076C0001LL;
      *(_DWORD *)(v1 + 76) = 0;
      *(_WORD *)(v1 + 80) = 0;
      *(_QWORD *)(v1 + 82) = 4279500900LL;
      *(_BYTE *)(v1 + 90) = 0;
      *(_QWORD *)v1 = 0x14187EB18LL;
      break;
    case 5:
      if ( dword_141B5CE88 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B5CE88);
        if ( dword_141B5CE88 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B5CE38,
            a2: 1100128687,
            a3: 128,
            a4: 32,
            a5: 0,
            a6: 0,
            a7: 128,
            a8: 4096);
          sub_141751048(a1: sub_140DF2BA0);
          sub_141750EA0(a1: &dword_141B5CE88);
        }
      }
      v1 = sub_1407E58C0(a1: &unk_141B5CE38, a2: 32);
      *(_QWORD *)v1 = 0x141878B08LL;
      *(_WORD *)(v1 + 30) = 0;
      *(_QWORD *)(v1 + 8) = 0;
      *(_QWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 21) = 0;
      break;
    default:
      v1 = 0;
      break;
  }
  return v1;
}
